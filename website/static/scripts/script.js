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