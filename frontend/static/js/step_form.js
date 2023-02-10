
initMultiStepForm();

function handleAccomodation(){
    var accomodation = $('#accomodation').find(":selected").text();
    console.log(accomodation);
    if(accomodation == 'Yes'){
        $('#accomodation_choice').show();
    }
    else{
        $('#accomodation_choice').hide();
    }
}

function initMultiStepForm() {
    const progressNumber = document.querySelectorAll(".step").length;
    const slidePage = document.querySelector(".slide-page");
    const submitBtn = document.querySelector(".submit");
    const progressText = document.querySelectorAll(".step p");
    const progressCheck = document.querySelectorAll(".step .check");
    const bullet = document.querySelectorAll(".step .bullet");
    const pages = document.querySelectorAll(".page");
    const nextButtons = document.querySelectorAll(".next");
    const prevButtons = document.querySelectorAll(".prev");
    const stepsNumber = pages.length;

    if (progressNumber !== stepsNumber) {
        console.warn(
            "Error, number of steps in progress bar do not match number of pages"
        );
    }

    document.documentElement.style.setProperty("--stepNumber", stepsNumber);

    let current = 1;

    for (let i = 0; i < nextButtons.length; i++) {
        nextButtons[i].addEventListener("click", function (event) {
            event.preventDefault();

            inputsValid = validateInputs(this);
            // inputsValid = true;

            if (inputsValid) {
                slidePage.style.marginLeft = `-${
                    (100 / stepsNumber) * current
                }%`;
                bullet[current - 1].classList.add("active");
                progressCheck[current - 1].classList.add("active");
                progressText[current - 1].classList.add("active");
                current += 1;
            }
        });
    }

    for (let i = 0; i < prevButtons.length; i++) {
        prevButtons[i].addEventListener("click", function (event) {
            event.preventDefault();
            slidePage.style.marginLeft = `-${
                (100 / stepsNumber) * (current - 2)
            }%`;
            bullet[current - 2].classList.remove("active");
            progressCheck[current - 2].classList.remove("active");
            progressText[current - 2].classList.remove("active");
            current -= 1;
        });
    }
    submitBtn.addEventListener("click", function (event) {

        inputsValid = validateInputs(this);
        // inputsValid = true;

        if (inputsValid) {
            bullet[current - 1].classList.add("active");
            progressCheck[current - 1].classList.add("active");
            progressText[current - 1].classList.add("active");
            current += 1;
        }
    });

    function validateInputs(ths) {
        let inputsValid = true;

        const inputs =
            ths.parentElement.parentElement.querySelectorAll("input");
        for (let i = 0; i < inputs.length; i++) {
            const valid = inputs[i].checkValidity();
            if (!valid) {
                inputsValid = false;
                inputs[i].classList.add("invalid-input");
            } else {
                inputs[i].classList.remove("invalid-input");
            }
        }
        return inputsValid;
    }
}

// (() => {
//   'use strict';

//   // Fetch all the forms we want to apply custom Bootstrap validation styles to
//   const forms = document.querySelectorAll('.needs-validation');

//   // Loop over them and prevent submission
//   Array.prototype.slice.call(forms).forEach((form) => {
//     form.addEventListener('submit', (event) => {
//       if (!form.checkValidity()) {
//         event.preventDefault();
//         event.stopPropagation();
//       }
//       form.classList.add('was-validated');
//     }, false);
//   });
// })();

// $(document).ready(function () {
//     $("#register_form").submit(function () {
//         $(".final-submit").attr("disabled", true);
//         return true;
//     });
// });

// FOR SWIMMING EVENTS
$(document).ready(function () {
    if(window.location.href.includes('swimming')){
        $("#total_amount").hide();
    }
});


function onSubmit(){

    let emails = document.querySelectorAll("input[name=player_emails]");
    let phone_numbers = document.querySelectorAll("input[name=player_phones]");
    let player_names = document.querySelectorAll("input[name=player_names]");

    if(emails.size()==phone_numbers.size() && emails.size()==player_names.size()){
        console.log("All enteries are correct")
    }
    else{
        console.log("Feilds missing")
    }

    event.preventDefault();

    if(window.location.href.includes('swimming')){
        $(".final-submit").attr("disabled", true);
        $("#loader").show();
        event.preventDefault();
        // get element by name jquery
        let emails = document.querySelectorAll("input[name=player_emails]");
        let email_list = [document.getElementsByName('email')[0].value];
        for (let i = 0; i < emails.length; i++) {
            email_list.push(emails[i].value);
        }
        // post api call
        var data = {
            'emails': email_list,
        };
        $.ajax({
            url: '/api/validateSwimming/',
            type: 'POST',
            data: data,
            success: function (data) {
                $("#loader").hide();
                for(let i = 0; i < data.length; i++){
                    if(!data[i]){
                        $("#unauthorizedEmailError").show();
                        $(".final-submit").attr("disabled", false);
                        $("#unauthorizedEmailError").text(`Player with email- ${email_list[i]} has already registered for 2 other Swimming events.`)
                        return;
                    }
                }
                $("#unauthorizedEmailError").show();
                $("#unauthorizedEmailError").text(`Redirecting to payment page...`)
                document.getElementById("register_form").submit();
            },
            error: function (data) {
                console.log(data);
            }
        });
    }
}