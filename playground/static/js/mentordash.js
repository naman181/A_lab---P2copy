     
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key == 'p') {
        alert('This section is not allowed to print or export to PDF');
        e.cancelBubble = true;
        e.preventDefault();
        e.stopImmediatePropagation();
    }
});
    
    function fun_Logout() {
        swal.fire({
            title: 'Are you sure?',
            text: "Do you really want to logout?",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Yes, Logout me!',
            cancelButtonText: 'No!',
            confirmButtonColor: '#d33',
            cancelButtonColor: '#202124',
            reverseButtons: true
        }).then((result) => {
            if (result.isConfirmed) {
                // Redirect to the login page
                window.location.href = "file:///Users/mohit/Desktop/New%20folder%20(9)/login.html";
            } else if (result.dismiss === Swal.DismissReason.cancel) {
                swal.fire(
                    'Cancelled',
                    'Logout cancelled.',
                    'error'
                )
            }
        });
    }

    function showNewClassroomForm() {

Swal.fire({
    html:
        '<div class="custom-title">Create Class</div>' +
        '<div style="text-align: left; font-family: Arial, Helvetica, sans-serif;">' +
            '<label for="class-name" >Class Name</label>' +
            '<input type="text" id="class-name" class="swal2-input" required>' +
            '<label for="section" >Section / Batch</label>' +
            '<input type="text" id="section" class="swal2-input" >' +
            '<label for="subject" >Subject</label>' +
            '<input type="text" id="subject" class="swal2-input" >' +
        '</div>',
    focusConfirm: false,
    showCancelButton: true, 
    confirmButtonText: '<span style="font-family: Arial, Helvetica, sans-serif;">Create</span>', 
    cancelButtonText: '<span style="font-family: Arial, Helvetica, sans-serif;">Cancel</span>', 
    preConfirm: () => {
        // Retrieve the entered values
        const className = Swal.getPopup().querySelector('#class-name').value;
        const section = Swal.getPopup().querySelector('#section').value;
        const subject = Swal.getPopup().querySelector('#subject').value;
      
        if (!className) {
            Swal.showValidationMessage('<span style="font-family: Arial, Helvetica, sans-serif;">Class Name is required</span>');
        }

        return { className, section, subject };
    }
}).then((result) => {
    // Check if the result contains values
    if (result.isConfirmed) {
        // Use the entered values as needed
        console.log('Class Name:', result.value.className);
        console.log('Section:', result.value.section);
        console.log('Subject:', result.value.subject);
    }
});
}

    function showContent(contentNumber) {
        for (let i = 1; i <= 5; i++) {
            var contentDiv = document.getElementById("content" + i);
            if (i === contentNumber) {
                contentDiv.classList.remove("hidden");
            } else {
                contentDiv.classList.add("hidden");
            }
        }
    }
