function delete_note(note_id) {
    fetch('/delete_note', {
        method: "POST",
        body: JSON.stringify({note_id: note_id})
    }).then((_res) => {
        window.location.href = "/"
    })
}

function toggle_completed(note_id) {
    fetch('/toggle_completed', {
        method: "POST",
        body: JSON.stringify({note_id: note_id})
    }).then((_res) => {
        window.location.href = "/"
    })
}

function toggle_popup() {
    var to_toggle = document.getElementById("pop_up");

    if (to_toggle.style.display == "block") {
        to_toggle.style.display = "none";
    } else {
        to_toggle.style.display = "block";
    }
}


window.onload=function() {
    var objDiv = document.getElementById("list");
    objDiv.scrollTo(0,-Number.MAX_SAFE_INTEGER)
}
