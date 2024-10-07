
function previewImage(event) {
    var input = event.target;
    var reader = new FileReader();

    reader.onload = function () {
        var preview = document.getElementById('logo-preview');
        preview.src = reader.result; 
        preview.style.display = 'block';
    };

    if (input.files && input.files[0]) {
        reader.readAsDataURL(input.files[0]); 
    }
}


function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

function confirmDelete(language_ID) {
    Swal.fire({
        title: 'Are you sure?',
        text: "Do you really want to delete this language?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!',
        cancelButtonText: 'Cancel',
        customClass: {
            popup: 'small-swal-popup',
            title: 'small-swal-title',
            content: 'small-swal-text',
            confirmButton: 'small-swal-button',
            cancelButton: 'small-swal-button',
            icon: 'small-swal-icon'
        }
    }).then((result) => {
        if (result.isConfirmed) {
            fetch(`/ringtone_lan/${language_ID}/delete/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    Swal.fire({
                        title: 'Deleted!',
                        text: 'The language has been deleted.',
                        confirmButtonColor: '#3085d6',
                        icon: 'success',
                        customClass: {
                            popup: 'small-swal-popup',
                            title: 'small-swal-title',
                            content: 'small-swal-text',
                            confirmButton: 'small-swal-button',
                            icon: 'small-swal-icon'
                        }
                    }).then(() => {
                        location.reload();
                    });
                } else {
                    Swal.fire({
                        title: 'Error!',
                        text: data.message,
                        icon: 'error',
                        customClass: {
                            popup: 'small-swal-popup',
                            title: 'small-swal-title',
                            content: 'small-swal-text',
                            confirmButton: 'small-swal-button',
                            icon: 'small-swal-icon'
                        }
                    });
                }
            })
            .catch(error => {
                Swal.fire({
                    title: 'Error!',
                    text: 'There was an error processing your request.',
                    icon: 'error',
                    customClass: {
                        popup: 'small-swal-popup',
                        title: 'small-swal-title',
                        content: 'small-swal-text',
                        confirmButton: 'small-swal-button',
                        icon: 'small-swal-icon'
                    }
                });
            });
        }
    });
}

function confirm_rington_Delete(ringtone_ID) {
    Swal.fire({
        title: 'Are you sure?',
        text: "Do you really want to delete this ringtone ?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!',
        cancelButtonText: 'Cancel',
        customClass: {
            popup: 'small-swal-popup',
            title: 'small-swal-title',
            content: 'small-swal-text',
            confirmButton: 'small-swal-button',
            cancelButton: 'small-swal-button',
            icon: 'small-swal-icon'
        }
    }).then((result) => {
        if (result.isConfirmed) {
            fetch(`/ringtones/${ringtone_ID}/delete/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    Swal.fire({
                        title: 'Deleted!',
                        text: 'The ringtone has been deleted.',
                        confirmButtonColor: '#3085d6',
                        icon: 'success',
                        customClass: {
                            popup: 'small-swal-popup',
                            title: 'small-swal-title',
                            content: 'small-swal-text',
                            confirmButton: 'small-swal-button',
                            icon: 'small-swal-icon'
                        }
                    }).then(() => {
                        location.reload();
                    });
                } else {
                    Swal.fire({
                        title: 'Error!',
                        text: data.message,
                        icon: 'error',
                        customClass: {
                            popup: 'small-swal-popup',
                            title: 'small-swal-title',
                            content: 'small-swal-text',
                            confirmButton: 'small-swal-button',
                            icon: 'small-swal-icon'
                        }
                    });
                }
            })
            .catch(error => {
                Swal.fire({
                    title: 'Error!',
                    text: 'There was an error processing your request.',
                    icon: 'error',
                    customClass: {
                        popup: 'small-swal-popup',
                        title: 'small-swal-title',
                        content: 'small-swal-text',
                        confirmButton: 'small-swal-button',
                        icon: 'small-swal-icon'
                    }
                });
            });
        }
    });
}


function userconfirmDelete(user_ID) {
    Swal.fire({
        title: 'Are you sure?',
        text: "Do you really want to delete this user ?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!',
        cancelButtonText: 'Cancel',
        customClass: {
            popup: 'small-swal-popup',
            title: 'small-swal-title',
            content: 'small-swal-text',
            confirmButton: 'small-swal-button',
            cancelButton: 'small-swal-button',
            icon: 'small-swal-icon'
        }
    }).then((result) => {
        if (result.isConfirmed) {
            fetch(`/users/${user_ID}/delete/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    Swal.fire({
                        title: 'Deleted!',
                        text: 'The user has been deleted.',
                        confirmButtonColor: '#3085d6',
                        icon: 'success',
                        customClass: {
                            popup: 'small-swal-popup',
                            title: 'small-swal-title',
                            content: 'small-swal-text',
                            confirmButton: 'small-swal-button',
                            icon: 'small-swal-icon'
                        }
                    }).then(() => {
                        location.reload();
                    });
                } else {
                    Swal.fire({
                        title: 'Error!',
                        text: data.message,
                        icon: 'error',
                        customClass: {
                            popup: 'small-swal-popup',
                            title: 'small-swal-title',
                            content: 'small-swal-text',
                            confirmButton: 'small-swal-button',
                            icon: 'small-swal-icon'
                        }
                    });
                }
            })
            .catch(error => {
                Swal.fire({
                    title: 'Error!',
                    text: 'There was an error processing your request.',
                    icon: 'error',
                    customClass: {
                        popup: 'small-swal-popup',
                        title: 'small-swal-title',
                        content: 'small-swal-text',
                        confirmButton: 'small-swal-button',
                        icon: 'small-swal-icon'
                    }
                });
            });
        }
    });
}




function RingtoneToggleStatus(id) {
    const checkbox = document.querySelector(`input[type="checkbox"][onchange="RingtoneToggleStatus(${id})"]`);
    const newStatus = checkbox.checked ? 1 : 0;

    // AJAX request
    fetch(`/ringtones/${id}/update_status/`, { 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ status: newStatus })
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Failed to update status');
        }
    })
    .then(data => {
        console.log(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
        checkbox.checked = !checkbox.checked;
    });
}


function toggleStatus(id) {
    const checkbox = document.querySelector(`input[type="checkbox"][onchange="toggleStatus(${id})"]`);
    const newStatus = checkbox.checked ? 1 : 0; // Assuming 1 is for active and 0 is for inactive

    // AJAX request
    fetch(`/ringtone_lan/${id}/update_status/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ status: newStatus })
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Failed to update status');
        }
    })
    .then(data => {
        console.log(data.message); // You can show a success message here
    })
    .catch(error => {
        console.error('Error:', error);
        // Optionally, revert the checkbox to its previous state if there's an error
        checkbox.checked = !checkbox.checked; // Revert status
    });
}

// Function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie string begins with the name we want
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// Music play function
let currentlyPlayingAudio = null;
function togglePlayback(id) {
    const audio = document.getElementById('audio' + id);
    const svg = document.getElementById('playable' + id);
    const playControl = svg.querySelector('.control.play');
    const pauseControl = svg.querySelector('.control.pause');
    const progressBar = svg.querySelector('.progress-bar');

    // Pause the currently playing audio if it's not the same as the clicked one
    if (currentlyPlayingAudio && currentlyPlayingAudio !== audio) {
        currentlyPlayingAudio.pause();
        const currentSvg = document.getElementById('playable' + currentlyPlayingAudio.id.replace('audio', ''));
        currentSvg.querySelector('.control.play').style.display = 'block'; // Show play icon
        currentSvg.querySelector('.control.pause').style.display = 'none'; // Hide pause icon
        resetProgress(currentSvg.querySelector('.progress-bar'));
    }

    // Handle play/pause toggle for the clicked audio
    if (audio.paused) {
        audio.play();
        playControl.style.display = 'none'; // Hide play icon
        pauseControl.style.display = 'block'; // Show pause icon
        currentlyPlayingAudio = audio; // Set the new playing audio
        updateProgress(audio, progressBar);
    } else {
        audio.pause();
        playControl.style.display = 'block'; // Show play icon
        pauseControl.style.display = 'none'; // Hide pause icon
        currentlyPlayingAudio = null; // Reset the currently playing audio
    }

    // When audio ends, reset icons and progress
    audio.addEventListener('ended', () => {
        playControl.style.display = 'block'; // Show play icon when audio ends
        pauseControl.style.display = 'none'; // Hide pause icon
        resetProgress(progressBar);
        currentlyPlayingAudio = null; // No audio is playing now
    });
}

// Function to update progress of the audio playback
function updateProgress(audio, progressBar) {
    const update = () => {
        if (!audio.paused && audio.duration) {
            const percent = (audio.currentTime / audio.duration) * 100;
            const dashArray = percent + ' ' + (100 - percent);
            progressBar.style.strokeDasharray = dashArray; // Set the dash array for progress

            // Continue updating the progress
            requestAnimationFrame(update);
        }
    };
    update();
}

// Function to reset progress
function resetProgress(progressBar) {
    progressBar.style.strokeDasharray = '0 100'; // Reset progress bar
}


// Ensure the audio's metadata is loaded before playing (for duration)
document.querySelectorAll('audio.listen').forEach(audio => {
    audio.addEventListener('loadedmetadata', () => {
        const id = audio.id.replace('audio', ''); // Extract the ID from the audio element's ID
        const progressBar = document.getElementById('playable' + id).querySelector('.progress-bar');
        updateProgress(audio, progressBar);
    });
    
    // Optional: Ensure audio is ready to play
    audio.addEventListener('canplay', () => {
        console.log('Audio ready to play:', audio.src);
    });
});

// City dependency via state
$(document).ready(function() {
    var url = $('div[data-url]').data('url');
    $('#state').change(function() {
        var stateId = $(this).val();
        if(stateId) {
            $.ajax({
                url: url,
                type: 'GET',
                data: {
                    'state_id': stateId
                },
                success: function(response) {
                    console.log("Cities fetched successfully: ", response);
                    $('#city').empty();
                    $('#city').append('<option value="">Select City</option>');
                    $.each(response.cities, function(key, city) {
                        $('#city').append('<option value="' + city.id + '">' + city.name + '</option>');
                    });
                },
                error: function(xhr, status, error) {
                    console.log("Error: ", error);
                }
            });
        } else {
            $('#city').empty();
            $('#city').append('<option value="">Select City</option>');
        }
    });
});