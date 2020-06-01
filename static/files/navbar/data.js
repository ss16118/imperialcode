function notificationOnClick() {
    let notificationPanel = document.getElementById("u23");
    let indicator = document.getElementById("u21");
    let hidden = notificationPanel.style.display.localeCompare("none") == 0;

    if (hidden) {
        notificationPanel.style.display = "flex";
        notificationPanel.style.visibility = "visible";
        indicator.style.display = "flex";
    } else {
        notificationPanel.style.display = "none";
        indicator.style.display = "none";
    }
}
