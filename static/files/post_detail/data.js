const COMMENT_PANEL_DEFAULT_HEIGHT = 103;
const COMMENT_CONTENT_DEFAULT_HEIGHT = 30;
const COMPONENT_DEFAULT_TOP = 74;
function createCommentPanel(index, topPos, author, commentContent, createdAt, upvotes) {
    let panelHTML = [
        `<div id="comment_${index}" class="ax_default box_2 u622" style="top: ${topPos}px;">`,
          `<div id="comment_div_${index}" class="u622_div ">`,
            '<div id="" class="ax_default heading_1 u623">',
              '<div id="" class="u623_div "></div>',
              '<div id="" class="text u623_text">',
                `<p><span>${author}</span></p>`,
              '</div>',
            '</div>',
            `<div id="comment_time_${index}" class="ax_default heading_1 time_label">`,
              '<div id="" class="time_label_div "></div>',
              '<div id="" class="text time_label_text">',
                `<p><span>Created at: ${createdAt}</span></p>`,
              '</div>',
            '</div>',
            '<div id="" class="ax_default paragraph u624">',
              '<div id="" class="u624_div "></div>',
              '<div id="" class="text u624_text">',
                `<p id="comment_content_${index}">${commentContent}</p>`,
              '</div>',
            '</div>',
            `<div id="comment_upvote_${index}" class="ax_default paragraph u625">`,
              '<div id="" class="u625_div "></div>',
              '<div id="" class="text u625_text">',
                '<p><span>⯅</span></p>',
              '</div>',
            '</div>',
            `<div id="comment_downvote_${index}" class="ax_default paragraph u626">`,
              '<div id="" class="u626_div "></div>',
              '<div id="" class="text u626_text">',
                '<p><span>⯆</span></p>',
              '</div>',
            '</div>',
            `<div id="comment_upvotes_label_${index}" class="ax_default heading_1 u627">`,
              '<div id="" class="u627_div "></div>',
              '<div id="" class="text u627_text">',
                `<p><span>${upvotes}</span></p>`,
              '</div>',
            '</div>',
            `<div id="comment_reply_button_${index}" class="ax_default paragraph u628">`,
              '<div id="" class="u628_div "></div>',
              '<div id="" class="text u628_text">',
                '<p><span>➥ Reply</span></p>',
              '</div>',
            '</div>',
          '</div>',
        '</div>'
    ].join("\n");
    let commentPanel = document.createElement("div");
    commentPanel.innerHTML = panelHTML;
    return commentPanel;
}