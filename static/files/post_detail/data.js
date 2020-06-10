const COMMENT_PANEL_DEFAULT_HEIGHT = 103;
const COMMENT_CONTENT_DEFAULT_HEIGHT = 30;
const COMPONENT_DEFAULT_TOP = 74;
let tempEditPostContent = "";
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

function togglePostPreview() {
  let previewButtonText = document.getElementById("post_content_preview_text");
  let contentAreaContainer = document.getElementById("u579");
  let isEditMode = previewButtonText.innerText.localeCompare("Preview") == 0;

  if (isEditMode) {
      let contentArea = document.getElementById("post_content_area");
      tempEditPostContent = contentArea.value;
      tempTextArea = contentArea;
      let displayBlock = document.createElement("div");
      displayBlock.id = "temp_post";

      displayBlock.style.padding = "1em";
      displayBlock.style.zIndex = 1000;
      displayBlock.style.height = postTextHeight + "px";
      displayBlock.style.overflow = "auto";
      displayBlock.innerHTML = marked(tempEditPostContent);
      contentAreaContainer.removeChild(contentArea);
      contentAreaContainer.appendChild(displayBlock);
      previewButtonText.innerHTML = "Edit";
  } else {
      let displayBlock = document.getElementById("temp_post");
      tempTextArea.value = tempEditPostContent;
      contentAreaContainer.removeChild(displayBlock);
      contentAreaContainer.appendChild(tempTextArea);
      previewButtonText.innerHTML = "Preview";
  }
}

function activateTab() {
  $("textarea").keydown(function (e) {
    if (e.keyCode === 9) { // tab was pressed
      // get caret position/selection
      var start = this.selectionStart;
      end = this.selectionEnd;

      var $this = $(this);

      // set textarea value to: text before caret + tab + text after caret
      $this.val($this.val().substring(0, start)
          + "\t"
          + $this.val().substring(end));

      // put caret at right position again
      this.selectionStart = this.selectionEnd = start + 1;
      // prevent the focus lose
      return false;
    }
  });
}