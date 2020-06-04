const INITIAL_POS_TOP = 60;
const PANEL_HEIGHT = 75;
const PADDING = 5;

function addNewPostButtonOnClick() {
    let newPostPanel = document.getElementById("u471");
    newPostPanel.style.visibility = "visible";
    newPostPanel.style.display = "flex";
}

function createPostPanel(link, num, author, title, createdAt, upvotes, commentNum, views) {
    let topPos = (INITIAL_POS_TOP + (num * (PANEL_HEIGHT + PADDING))) + "px";
    let panelHTML = [
        `<a href="${link}">`,
        `<div id="u423" class="ax_default box_1" style="top:${topPos}">`,
          '<div id="u423_div" class="">',
            '<div id="u424" class="ax_default heading_1">',
              '<div id="u424_div" class=""></div>',
              '<div id="u424_text" class="text ">',
                `<p><span>${title}</span></p>`,
              '</div>',
            '</div>',
            '<div id="u425" class="ax_default heading_1">',
              '<div id="u425_div" class=""></div>',
              '<div id="u425_text" class="text ">',
                `<p><span>Created by ${author} ${createdAt}</span></p>`,
              '</div>',
            '</div>',
            '<div id="u426" class="ax_default heading_1">',
              '<div id="u426_div" class=""></div>',
              '<div id="u426_text" class="text ">',
                `<p><span>▲ ${upvotes}</span></p>`,
              '</div>',
            '</div>',
            '<div id="u427" class="ax_default heading_1">',
              '<div id="u427_div" class=""></div>',
              '<div id="u427_text" class="text ">',
                `<p><span>🗨 ${commentNum}</span></p>`,
              '</div>',
            '</div>',
            '<div id="u428" class="ax_default heading_1">',
              '<div id="u428_div" class=""></div>',
              '<div id="u428_text" class="text ">',
                `<p><span>👁 ${views}</span></p>`,
              '</div>',
            '</div>',
          '</div>',
        '<\div>'
    ].join("\n");
    return panelHTML;
}