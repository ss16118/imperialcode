const EDITOR_DEFAULT_WIDTH = 574;
const EDITOR_DEFAULT_HEIGHT = 357;
const EDITOR_EXPAND_WIDTH = 1268;
const EDITOR_EXPAND_HEIGHT = 581;
const DEFAULT_X = 713;
const EXPAND_X = 19;

const PROGRESS_WARNING_MESSAGE =
    `Warning: you have not completed all the previous subquestions.\n---------------------------------------------\n`;

function testcaseConsoleOnclick() {
    let testcaseButton = document.getElementById("u269_div");
    let outputButton = document.getElementById("u270_div");

    outputButton.className = outputButton.className.replace(" selected", "");
    testcaseButton.className = testcaseButton.className.replace(" selected", "");
    testcaseButton.className += " selected";

    let testcaseArea = document.getElementById("u274");
    let outputArea = document.getElementById("u277");

    outputArea.style.display = "none";
    testcaseArea.style.display = "flex";
}

function outputConsoleOnclick() {
    let testcaseButton = document.getElementById("u269_div");
    let outputButton = document.getElementById("u270_div");

    testcaseButton.className = testcaseButton.className.replace(" selected", "");
    outputButton.className = outputButton.className.replace(" selected", "");
    outputButton.className += " selected";

    let outputArea = document.getElementById("u277");
    let testcaseArea = document.getElementById("u274");

    testcaseArea.style.display = "none";
    outputArea.style.display = "flex";
}


function hideConsoleOnClick() {
    let buttonText = document.getElementById("u282_text");
    let hidden = buttonText.innerHTML.localeCompare("Hide console ⯅") == 0;

    let editor = $('.CodeMirror')[0].CodeMirror;

    if (hidden) {
        editor.setSize(null, EDITOR_DEFAULT_HEIGHT);
        buttonText.innerHTML = "Hide console ⯆";
    } else {
        editor.setSize(null, EDITOR_EXPAND_HEIGHT);
        buttonText.innerHTML = "Hide console ⯅";
    }

    editor.refresh();
}

function hideSpecOnClick() {
    let buttonText = document.getElementById("u281_text");
    let hidden = buttonText.innerHTML.localeCompare("⯈") == 0;
    let wrapper = document.getElementById("u278");
    let spec = document.getElementById("u279");
    let singleQuestion = document.getElementById("u280");

    let testcaseButton = document.getElementById("u269");
    let outputButton = document.getElementById("u270");
    let testcaseArea = document.getElementById("u274");
    let outputArea = document.getElementById("u277");

    let editor = $('.CodeMirror')[0].CodeMirror;

    if (hidden) {
        editor.setSize(EDITOR_DEFAULT_WIDTH, null);

        spec.style.visibility = "visible";
        singleQuestion.style.visibility = "visible";

        wrapper.style.left = DEFAULT_X + "px";
        wrapper.style.width = EDITOR_DEFAULT_WIDTH + "px";

        buttonText.innerHTML = "⯇";

        testcaseButton.style.left = DEFAULT_X + "px";
        outputButton.style.left = "817px";
        testcaseArea.style.left = DEFAULT_X + "px";
        resizeTextAreaWidth(testcaseArea.id, EDITOR_DEFAULT_WIDTH);
        outputArea.style.left = DEFAULT_X + "px";
        resizeTextAreaWidth(outputArea.id, EDITOR_DEFAULT_WIDTH);

    } else {
        editor.setSize(EDITOR_EXPAND_WIDTH, null);

        spec.style.visibility = "hidden";
        singleQuestion.style.visibility = "hidden";

        wrapper.style.left = "19px";
        wrapper.style.width = EDITOR_EXPAND_WIDTH + "px";

        buttonText.innerHTML = "⯈";

        testcaseButton.style.left = EXPAND_X + "px";
        outputButton.style.left = "124px";
        testcaseArea.style.left = EXPAND_X + "px";
        resizeTextAreaWidth(testcaseArea.id, EDITOR_EXPAND_WIDTH);
        outputArea.style.left = EXPAND_X + "px";
        resizeTextAreaWidth(outputArea.id, EDITOR_EXPAND_WIDTH);
    }

    editor.refresh();
}

function showSubquestionsOnClick() {
    let subquestionsPanel = document.getElementById("u328");
    subquestionsPanel.style.display = "flex";
    subquestionsPanel.style.visibility = "visible";
}

window.onclick = function(event) {
    let subquestionsPanel = document.getElementById("u328");
    if (event.target == subquestionsPanel) {
        subquestionsPanel.style.display = "none";
    }
}

let resizeTextAreaWidth = function(componentId, newWidth) {
    let component = document.getElementById(componentId);
    component.style.width = newWidth + "px";
    let componentDiv = document.getElementById(componentId + "_div");
    componentDiv.style.width = newWidth + "px";
    let componentInput = document.getElementById(componentId + "_input");
    componentInput.style.width = newWidth + "px";
}


function editorSettingsButtonOnClick() {
    let editorSettingsPanel = document.getElementById("u353");
    editorSettingsPanel.style.display = "flex";
    editorSettingsPanel.style.visibility = "visible";
}

function editorSettingsCancelButtonOnClick() {
    let editorSettingsPanel = document.getElementById("u353");
    editorSettingsPanel.style.display = "none";
}

const LABEL_INITIAL_TOP_POS = 115;
const LABEL_PADDING = 15;
const LABEL_HEIGHT = 18;

function createNavigationLabel(index, title) {
    let topPos = (LABEL_INITIAL_TOP_POS  + (index * (LABEL_HEIGHT + LABEL_PADDING))) + "px";
    let labelHTML = [
        `<div id=u333 class="ax_default heading_3" style="top:${topPos}" onclick="displaySubquestion(${index})">`,
          '<div id="u333_div" class=""></div>',
          '<div id="u333_text" class="text subquestion">',
            `<p>Question ${index + 1}: ${title}</p>`,
          '</div>',
        '</div>'
    ].join("\n");
    return labelHTML;
}

function passedTest(funcName, outputMessage) {
    let pattern = new RegExp(`\\b(?:\\w+): (\\d+) \/ (\\d+)\\b`, "g");
    let match = pattern.exec(outputMessage);
    if (match !== null) {
        return match[1].localeCompare(match[2]) == 0;
    }
    return false;
}

function finishedPrevSubquestions(finishedSubquestions, currentSubquestion) {
    for (let i = 0; i < currentSubquestion; i++) {
        if (!finishedSubquestions.includes(i)) {
            return false;
        }
    }
    return true;
}

function saveEditorSettings() {
    let fontSizeField = document.getElementById("u359_input");
    let themeField = document.getElementById("u357_input");
    let keyBindingField = document.getElementById("u355_input");

    let fontSize = fontSizeField.value;
    let theme = themeField.value;
    let keyBinding = keyBindingField.value;

    let editor = $('.CodeMirror')[0].CodeMirror;
    editor.getWrapperElement().style["font-size"] = fontSize;
    editor.setOption("keyMap", keyBinding);
    editor.setOption("theme", theme);

    $.ajax({
        type: "POST",
        url: "/save_editor_settings/",
        async: false,
        data: {
            "font_size": fontSize,
            "theme": theme,
            "key_binding": keyBinding,
            "csrfmiddlewaretoken": window.CSRF_TOKEN
        },
        success: function (_) {}
    });
    editorSettingsCancelButtonOnClick();
}