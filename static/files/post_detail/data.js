const COMMENT_PANEL_DEFAULT_HEIGHT = 103;
const COMMENT_CONTENT_DEFAULT_HEIGHT = 30;
const COMPONENT_DEFAULT_TOP = 74;
let tempEditPostContent = "";
let tempEditCommentContent = "";
let tempTextArea = null;
let commentContents = {};
let commentMarkdownBlocks = {};
let editCommentContents = {};
let commentContentEditors = {};
let commentIds = [];
let mainPostId = 0;
let commentIdToVote = {};
function createCommentPanel(index, commentId, topPos, author, commentContent, createdAt, upvotes, editable) {
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
            `<div id="comment_content_container_${index}" class="ax_default paragraph u624">`,
              '<div id="" class="u624_div "></div>',
              `<div id="comment_content_text_${index}" class="text u624_text">`,
                `<p id="comment_content_${index}"></p>`,
              '</div>',
            '</div>',
            `<div id="comment_upvote_${index}" class="ax_default paragraph comment_vote_${commentId} u625" onclick="registerVote('comment_vote_${commentId}', ${commentId}, UP, 'comment_upvotes_label_text_${index}')">`,
              `<div id="comment_upvote_${index}_div" class="u625_div "></div>`,
              '<div id="" class="text u625_text">',
                '<p><span>⯅</span></p>',
              '</div>',
            '</div>',
            `<div id="comment_downvote_${index}" class="ax_default paragraph comment_vote_${commentId} u626" onclick="registerVote('comment_vote_${commentId}', ${commentId}, DOWN, 'comment_upvotes_label_text_${index}')">`,
              `<div id="comment_downvote_${index}_div" class="u626_div "></div>`,
              '<div id="" class="text u626_text">',
                '<p><span>⯆</span></p>',
              '</div>',
            '</div>',
            `<div id="comment_upvotes_label_${index}" class="ax_default heading_1 u627">`,
              '<div id="" class="u627_div "></div>',
              `<div id="comment_upvotes_label_text_${index}" class="text u627_text">`,
                `<p><span>${upvotes}</span></p>`,
              '</div>',
            '</div>',
            `<div id="comment_reply_button_${index}" class="ax_default paragraph u628">`,
              '<div id="" class="u628_div "></div>',
              '<div id="" class="text u628_text">',
                '<p><span>➥ Reply</span></p>',
              '</div>',
            '</div>'];
    panelHTML = editable ? panelHTML.concat([
          `<div id="comment_preview_${index}" class="ax_default button comment_preview" onclick="commentTogglePreview(${index})">`,
            '<div id="" class="comment_preview_div"></div>',
            `<div id="comment_preview_text_${index}" class="text comment_preview_text">`,
              'Preview',
            '</div>',
          '</div>',
          `<div id="comment_edit_${index}" class="ax_default label comment_edit" onclick="commentToggleEdit(${index})">`,
            '<div id="" class="comment_edit_div"></div>',
            `<div id="comment_edit_${index}" class="text comment_edit_text">`,
              '✒️Edit',
            '</div>',
          '</div>',
          `<div id="save_comment_${index}" class="ax_default label save_comment" onclick="saveCommentContent(${index})">`,
            '<div id="" class="save_comment_div"></div>',
              '<div id="" class="text save_comment_text">',
                '<p><span>Save</span></p>',
            '</div>',
          '</div>',
          `<div id="comment_delete_${index}" class="ax_default label comment_delete" onclick="deleteComment(${commentIds[index]})">`,
            '<div id="" class="text comment_delete_text"></div>',
            '<input type="submit" id="" class="comment_delete_div " value="🗑 Delete">',
          '</div>',
        '</div>', '</div>'
        ]) :
        panelHTML.concat('</div>', '</div>');
    commentContent = decode(commentContent);
    if (editable) {
        commentContents[index] = commentContent;
    }
    let commentPanel = document.createElement("div");
    commentPanel.innerHTML = panelHTML.join("\n");

    let descendants = commentPanel.querySelectorAll("*");
    for (let i = 0; i < descendants.length; i++) {
        if (descendants[i].id === `comment_content_${index}`) {
            descendants[i].innerHTML = marked(commentContent);
        }
    }
    return commentPanel;
}

let deleteComment = function(id) {
    $.ajax({
        type: "POST",
        url: "/delete_comment/",
        async: false, // Just to be safe
        data: {
            "id": id,
            "csrfmiddlewaretoken": window.CSRF_TOKEN
        },
        success: function(data) {
            if (id != mainPostId) {
                window.location.reload();
            } else {
                // Go back one page if the main post is deleted
                document.getElementById("u570").click();
            }
        }
    });
}

let saveCommentContent = function(index) {
    $.ajax({
        type: "POST",
        url: "/save_comment/",
        async: false, // Just to be safe
        data: {
            "id": commentIds[index],
            "content": commentContentEditors[index].value,
            "csrfmiddlewaretoken": window.CSRF_TOKEN
        },
        success: function(data) {
            window.location.reload();
        }
    });
};


let commentTogglePreview = function(index) {
    let commentPreviewButtonText = document.getElementById(`comment_preview_text_${index}`);
    let isEditMode = commentPreviewButtonText.innerText.localeCompare("Preview") === 0;
    let commentContentContainer = document.getElementById(`comment_content_container_${index}`);

    if (isEditMode) {
        commentPreviewButtonText.innerHTML = "Edit";
        let tempContent = commentContentEditors[index].value;
        editCommentContents[index] = tempContent;
        let tempCommentContentBlock = createMarkdownBlock(`temp_content_md_${index}`, tempContent,
                commentContentEditors[index].style.height, false);
        commentContentContainer.appendChild(tempCommentContentBlock);
        commentContentContainer.removeChild(commentContentEditors[index]);
    } else {
        commentPreviewButtonText.innerHTML = "Preview";
        let commentContentEditor = commentContentEditors[index];
        commentContentEditor.value = editCommentContents[index];
        commentContentContainer.appendChild(commentContentEditor);
        commentContentContainer.removeChild(document.getElementById(`temp_content_md_${index}`));
    }
}


let commentToggleEdit = function(index) {
    let commentEditButtonText = document.getElementById(`comment_edit_${index}`);
    let isEditMode = commentEditButtonText.innerHTML.localeCompare("Cancel") == 0;
    let commentPreviewButton = document.getElementById(`comment_preview_${index}`);
    let commentSaveButton = document.getElementById(`save_comment_${index}`);
    let commentDeleteButton = document.getElementById(`comment_delete_${index}`);
    let commentContentContainer = document.getElementById(`comment_content_container_${index}`);

    if (isEditMode) {
        commentEditButtonText.innerHTML = "✒️Edit";
        commentDeleteButton.style.display = "flex";
        commentPreviewButton.style.display = "none";
        commentSaveButton.style.display = "none";
        document.getElementById(`comment_preview_text_${index}`).innerHTML = "Preview";

        let commentContentEditor = document.getElementById(`comment_editor_${index}`);

        if (commentContentEditor !== null) {
            commentContentContainer.removeChild(commentContentEditor);
        } else {
            commentContentContainer.removeChild(document.getElementById(`temp_content_md_${index}`));
        }
        commentContentContainer.appendChild(commentMarkdownBlocks[index]);
    } else {
        commentEditButtonText.innerHTML = "Cancel";
        commentDeleteButton.style.display = "none";
        commentPreviewButton.style.display = "flex";
        commentSaveButton.style.display = "flex";

        // Create a textarea that surrounds the comment content
        let commentContentEditor = document.createElement("textarea");
        let commentContentBlock = commentMarkdownBlocks[index];
        commentContentEditor.style.height = commentContentBlock.getBoundingClientRect().height + 10 + "px";
        commentContentEditor.id = `comment_editor_${index}`;
        commentContentEditor.classList += "comment_editor";
        commentContentEditor.value = commentContents[index];
        commentContentEditors[index] = commentContentEditor;

        commentContentContainer.appendChild(commentContentEditor);
        commentContentContainer.removeChild(commentContentBlock);
    }
};

function togglePostPreview() {
  let previewButtonText = document.getElementById("post_content_preview_text");
  let contentAreaContainer = document.getElementById("u579");
  let isEditMode = previewButtonText.innerText.localeCompare("Preview") == 0;

  if (isEditMode) {
      let contentArea = document.getElementById("post_content_area");
      tempEditPostContent = contentArea.value;
      tempTextArea = contentArea;
      let displayBlock = createMarkdownBlock("temp_post", tempEditPostContent, contentArea.style.height);
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

function toggleCommentPreview() {
  let previewButtonText = document.getElementById("u641_text");
  let contentAreaContainer = document.getElementById("u618");
  let isEditMode = previewButtonText.innerText.localeCompare("Preview") == 0;

  if (isEditMode) {
      let contentArea = document.getElementById("u618_input");
      tempEditCommentContent = contentArea.value;
      tempTextArea = contentArea;
      let displayBlock = createMarkdownBlock("temp_comment", tempEditCommentContent, contentArea.style.height);
      contentArea.style.display = "none";
      contentAreaContainer.appendChild(displayBlock);
      previewButtonText.innerHTML = "Edit";
  } else {
      let displayBlock = document.getElementById("temp_comment");
      tempTextArea.value = tempEditCommentContent;
      contentAreaContainer.removeChild(displayBlock);
      tempTextArea.style.display = "flex";
      previewButtonText.innerHTML = "Preview";
  }
}
function createMarkdownBlock(id, textContent, blockHeight, padding=true) {
    let displayBlock = document.createElement("div");
    displayBlock.id = id;
    if (padding) {
        displayBlock.style.padding = "1em";
    }
    displayBlock.style.zIndex = "1000";
    displayBlock.style.height = blockHeight;
    displayBlock.style.overflow = "auto";
    displayBlock.innerHTML = marked(textContent);
    return displayBlock;
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

function togglePostEdit() {
    let editButtonText = document.getElementById("u639_text");
    let isPostEditMode = editButtonText.innerText.localeCompare("Cancel") == 0;
    let previewButton = document.getElementById("post_content_preview");
    let titleContainer = document.getElementById("u571");
    let contentContainer = document.getElementById("u579");
    let deleteButton = document.getElementById("u640");
    let saveButton = document.getElementById("save_post");

    if (isPostEditMode) {
        previewButton.style.display = "none";
        document.getElementById("post_content_preview_text").innerHTML = "Preview";
        let titleEditor = document.getElementById("title_field");
        titleContainer.removeChild(titleEditor);
        titleContainer.appendChild(tempTitleText);

        let contentEditor = document.getElementById("post_content_area");
        if (contentEditor !== null) {
            contentContainer.removeChild(contentEditor);
        } else {
            contentContainer.removeChild(document.getElementById("temp_post"));
        }
        contentContainer.appendChild(tempPostContent);

        deleteButton.style.display = "flex";
        saveButton.style.display = "none";
        editButtonText.innerHTML = "✒️Edit";
    } else {
        previewButton.style.display = "flex";

        let titleEditor = document.createElement("input");
        titleEditor.id = "title_field";
        titleEditor.name = "post_title";
        titleEditor.value = tempTitleText.innerText;

        titleContainer.removeChild(tempTitleText);
        titleContainer.appendChild(titleEditor);

        let contentEditor = document.createElement("textarea");
        contentEditor.id = "post_content_area";
        contentEditor.name = "post_content_field";
        contentEditor.style.height = postTextHeight + 25 + "px";
        contentEditor.value = postContent;

        contentContainer.removeChild(tempPostContent);
        contentContainer.appendChild(contentEditor);

        activateTab();
        deleteButton.style.display = "none";
        saveButton.style.display = "flex";
        editButtonText.innerHTML = "Cancel";
    }
}

let decode = function(encodedString) {
    return $("<p/>").html(encodedString).text();
};

/* Display Votes */
const UP = 1;
const NO_VOTE = 0;
const DOWN = -1;

let toggleUpvoteButton = function(button, activate) {
    button.style.color = activate ? "black" : "gray";
    let buttonDiv = document.getElementById(`${button.id}_div`);
    buttonDiv.style.backgroundColor = activate ? "salmon" : "transparent";
    if (activate) {
        button.onmouseover = function () {
            button.style.color = "gray";
            buttonDiv.style.backgroundColor = "transparent";
        }
        button.onmouseout = function () {
            button.style.color = "black";
            buttonDiv.style.backgroundColor = "salmon";
        }
    } else {
        button.onmouseover = function () {
            button.style.color = "black";
            buttonDiv.style.backgroundColor = "salmon";
        }
        button.onmouseout = function () {
            button.style.color = "gray";
            buttonDiv.style.backgroundColor = "transparent";
        }
    }
}
let toggleDownvoteButton = function(button, activate) {
    button.style.color = activate ? "black" : "gray";
    let buttonDiv = document.getElementById(`${button.id}_div`);
    buttonDiv.style.backgroundColor = activate ? "lightblue" : "transparent";
    if (activate) {
        button.onmouseover = function () {
            button.style.color = "gray";
            buttonDiv.style.backgroundColor = "transparent";
        }
        button.onmouseout = function () {
            button.style.color = "black";
            buttonDiv.style.backgroundColor = "lightblue";
        }
    } else {
        button.onmouseover = function () {
            button.style.color = "black";
            buttonDiv.style.backgroundColor = "lightblue";
        }
        button.onmouseout = function () {
            button.style.color = "gray";
            buttonDiv.style.backgroundColor = "transparent";
        }
    }
}

function displayVote(buttonGroupName, userVote) {
    let buttonGroup = document.getElementsByClassName(buttonGroupName);
    let upvoteButton = buttonGroup[0];
    let downvoteButton = buttonGroup[1];

    if (userVote == UP) {
        toggleDownvoteButton(downvoteButton, false);
        toggleUpvoteButton(upvoteButton, true);
    } else if (userVote == DOWN) {
        toggleDownvoteButton(downvoteButton, true);
        toggleUpvoteButton(upvoteButton, false);
    } else {
        toggleDownvoteButton(downvoteButton, false);
        toggleUpvoteButton(upvoteButton, false);
    }
}

function registerVote(buttonGroupName, commentId, type, labelId) {
    let userVote = commentIdToVote[commentId]
    type = Math.abs(type - userVote) < 2 ? (userVote + type) % 2 : type;
    let diff = type - userVote;
    let upvoteLabel = document.getElementById(labelId);
    upvoteLabel.innerHTML = parseInt(upvoteLabel.innerText) + diff;
    commentIdToVote[commentId] = type;
    displayVote(buttonGroupName, type);
    $.ajax({
        type: "POST",
        url: "/register_comment_vote/",
        async: false,
        data: {
            "id": commentId,
            "type": type,
            "csrfmiddlewaretoken": window.CSRF_TOKEN
        },
        success: function(_) {
        }
    });
}