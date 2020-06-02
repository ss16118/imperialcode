function expandNewPostButtonOnClick() {
    let expandButton = document.getElementById("u474");
    let closeButton = document.getElementById("u475");
    let postButton = document.getElementById("u476");
    let titleField = document.getElementById("u477");
    let dummyImage = document.getElementById("u478");
    let descriptionArea = document.getElementById("u479");
    let divider = document.getElementById("u480");
    let panel = document.getElementById("u473");

    let components = [expandButton, closeButton, postButton, titleField, dummyImage, descriptionArea, divider, panel];
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
    console.log(expanded);
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