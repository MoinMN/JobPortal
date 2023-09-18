let edit = document.getElementsByClassName('edit');
        let submit = document.getElementsByClassName('submit');

        let profileForm = document.getElementsByClassName('profileForm');
        let addressForm = document.getElementsByClassName('addressForm');
        let educationForm = document.getElementsByClassName('educationForm');
        let experienceForm = document.getElementsByClassName('experienceForm');

        let dateEdu = document.getElementsByClassName('dateEdu');
        let dateTextEdu = document.getElementsByClassName('dateTextEdu');
        let dateExp = document.getElementsByClassName('dateExp');
        let dateTextExp = document.getElementsByClassName('dateTextExp');

        let skillsInput = document.getElementById('skillsInput');
        let skillsOutput = document.getElementById('skillsOutput');

        for (let i = 0; i < edit.length; i++) {
            edit[i].addEventListener("click", () => {
                edit[i].style.display = 'none';
                submit[i].style.display = 'block';
                if (i == 0) {
                    for (var j = 0; j < profileForm.length; j++) {
                        skillsInput.style.display = 'block';
                        skillsOutput.style.display = 'none';
                        profileForm[j].removeAttribute('disabled');
                        profileForm[j].classList.add('bg');
                        profileForm[j].classList.remove('nobg');
                    }
                }
                else if (i == 1) {
                    for (var j = 0; j < addressForm.length; j++) {
                        addressForm[j].removeAttribute('disabled');
                        addressForm[j].classList.add('bg');
                        addressForm[j].classList.remove('nobg');
                    }
                }
                else if (i == 2) {
                    for (var j = 0; j < educationForm.length; j++) {
                        educationForm[j].removeAttribute('disabled');
                        educationForm[j].classList.add('bg');
                        educationForm[j].classList.remove('nobg');
                        for (var k = 0; k < 2; k++) {
                            dateTextEdu[k].style.display = 'none';
                            dateEdu[k].style.display = 'block';
                        }
                    }
                }
                else if (i == 3) {
                    for (var j = 0; j < experienceForm.length; j++) {
                        experienceForm[j].removeAttribute('disabled');
                        experienceForm[j].classList.add('bg');
                        experienceForm[j].classList.remove('nobg');
                        for (var k = 0; k < 2; k++) {
                            dateTextExp[k].style.display = 'none';
                            dateExp[k].style.display = 'block';
                        }
                    }
                }
                else {
                    console.log(Error);
                }
            });
            submit[i].addEventListener("click", () => {
                edit[i].style.display = 'block';
                submit[i].style.display = 'none';
            });
        }

        let radio = document.getElementsByName('menu');
        for (let i = 0; i < radio.length; i++) {
            radio[i].addEventListener("click", () => {
                if (radio[i].id == 'basic') {
                    document.getElementById("basicData").style.display = 'block';
                    document.getElementById("addressData").style.display = 'none';
                    document.getElementById("educationData").style.display = 'none';
                    document.getElementById("experienceData").style.display = 'none';
                }
                else if (radio[i].id == 'address') {
                    document.getElementById("basicData").style.display = 'none';
                    document.getElementById("addressData").style.display = 'block';
                    document.getElementById("educationData").style.display = 'none';
                    document.getElementById("experienceData").style.display = 'none';
                }
                else if (radio[i].id == 'education') {
                    document.getElementById("basicData").style.display = 'none';
                    document.getElementById("addressData").style.display = 'none';
                    document.getElementById("educationData").style.display = 'block';
                    document.getElementById("experienceData").style.display = 'none';
                }
                else {
                    document.getElementById("basicData").style.display = 'none';
                    document.getElementById("addressData").style.display = 'none';
                    document.getElementById("educationData").style.display = 'none';
                    document.getElementById("experienceData").style.display = 'block';
                }
            });
        }