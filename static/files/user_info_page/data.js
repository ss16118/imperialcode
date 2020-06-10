let initialTopPos = 95;
const DEFAULT_POST_PANEL_HEIGHT = 42;
const PANEL_PADDING = 5;
function createPostPanel(link, index, postTitle, postUpvotes, postCommentNum) {
    let topPos = initialTopPos + (DEFAULT_POST_PANEL_HEIGHT + PANEL_PADDING) * index + "px";
    let panelHTML = [
        `<a href="${link}">`,
          `<div id="" class="ax_default box_2 post_panel" style="top:${topPos}">`,
            '<div id="" class="post_panel_div "></div>',
              '<div id="" class="ax_default heading_1 post_title ">',
                '<div id="" class="post_title_div "></div>',
                '<div id="" class="text post_title_text ">',
                  `<p><span>${postTitle}</span></p>`,
                '</div>',
              '</div>',
              '<div id="" class="ax_default heading_1 post_upvotes">',
                '<div id="" class="post_upvotes_div "></div>',
                '<div id="" class="text post_upvotes_text">',
                  `<p><span>▲ ${postUpvotes}</span></p>`,
                '</div>',
              '</div>',
              '<div id="" class="ax_default heading_1 post_comments">',
                '<div id="" class="post_comments_div"></div>',
                '<div id="" class="text post_comments_text">',
                  `<p><span>🗨 ${postCommentNum}</span></p>`,
                '</div>',
              '</div>',
            '</div>',
          '</div>',
        '</a>'
    ].join("\n");
    let postPanel = document.createElement("div");
    postPanel.innerHTML = panelHTML;
    return postPanel;
}