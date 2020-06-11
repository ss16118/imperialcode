let postContent = "";
let tempTextArea = null;

function expandNewPostButtonOnClick() {
    let expandButton = document.getElementById("u474");
    let closeButton = document.getElementById("u475");
    let postButton = document.getElementById("u476");
    let titleField = document.getElementById("u477");
    let dummyImage = document.getElementById("u478");
    let descriptionArea = document.getElementById("u479");
    let divider = document.getElementById("u480");
    let previewButton = document.getElementById("u516");
    let panel = document.getElementById("u473");

    let components = [expandButton, closeButton, postButton, titleField, dummyImage,
        descriptionArea, divider, panel, previewButton];
    let expanded = expandButton.innerHTML.localeCompare("⮟") == 0;

    let posDif = expanded ? 277 : -277;

    components.forEach(comp => {
        comp.style.top = (comp.offsetTop + posDif) + "px";
    });

    if (expanded) {
        resizePanelHeight("u473", 359);
        resizePanelHeight("u479", 224);
        expandButton.innerHTML = "⮝";
    } else {
        resizePanelHeight("u473", 637);
        resizePanelHeight("u479", 502);
        expandButton.innerHTML = "⮟";
    }
}

let setCompOffsetTop = function(componentId, newTop) {
    let component = document.getElementById(componentId);
    component.style.top = newTop + "px";
    let componentDiv = document.getElementById(componentId + "_div");
    componentDiv.style.top = newTop + "px";
}


let resizePanelHeight = function(componentId, newHeight) {
    let component = document.getElementById(componentId);
    component.style.height = newHeight + "px";
    let componentDiv = document.getElementById(componentId + "_div");
    componentDiv.style.height = newHeight + "px";
    let componentInput = document.getElementById(componentId + "_input");
    if (componentInput !== null) {
        componentInput.style.height = newHeight + "px";
    }
}

function closeButtonOnClick() {
    let newPostPanel = document.getElementById("u471");
    newPostPanel.style.visibility = "hidden";
    newPostPanel.style.display = "none";
}

function togglePreview() {
    let previewButtonText = document.getElementById("u516_text");
    let contentAreaContainer = document.getElementById("u479");
    let isEditMode = previewButtonText.innerText.localeCompare("Preview") == 0;

    if (isEditMode) {
        let contentArea = document.getElementById("u479_input");
        newPostContent = contentArea.value;
        tempTextArea = contentArea;
        let displayBlock = document.createElement("div");
        displayBlock.id = "temp";
        displayBlock.style.padding = "1em";
        displayBlock.style.zIndex = 1500;
        displayBlock.innerHTML = marked(newPostContent);
        contentAreaContainer.removeChild(contentArea);
        contentAreaContainer.appendChild(displayBlock);
        previewButtonText.innerHTML = "Edit";
    } else {
        let displayBlock = document.getElementById("temp");
        tempTextArea.value = newPostContent;
        contentAreaContainer.removeChild(displayBlock);
        contentAreaContainer.appendChild(tempTextArea);
        previewButtonText.innerHTML = "Preview";
    }
}