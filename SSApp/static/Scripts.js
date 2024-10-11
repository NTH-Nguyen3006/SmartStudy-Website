function checkPasswordFormInput() {
    const input_tag = document.getElementsByName('password');
    var input_value = input_tag[0].value;
    console.log(input_value);

    if (input_value.trim()) {
        if (input_value.length < 8 || input_value.length > 20) {
            const box = document.getElementById(`password-box`);
            // const tagInput = document.getElementsByName(password)

            // Tạo thẻ div có các thuộc tính
            let create_div = create_valid_feedback(
                "Mật khẩu chỉ được nằm trong phạm vi 8 đến 20 kí tự");

            input_tag[0].className = 'form-control is-invalid';

            if (!box.querySelector('.invalid-feedback'))
                box.insertBefore(create_div, box.children[-1]);
        }
        else {
            const box = document.getElementById(`password-box`);

            // Tạo thẻ div có các thuộc tính
            let create_div = create_valid_feedback("valid", "Mật khẩu hợp lý");

            input_tag[0].className = 'form-control is-valid';

            if (!box.querySelector('.invalid-feedback'))
                box.insertBefore(create_div, box.children[-1]);
        }
    } else {
        document.getElementById(
            "validationServerFeedback").style = "dislay: none;";
        input_tag[0].className = 'form-control';
    }
}

function checkVerifyPassword() {
    const verify_password = document.getElementsByName('verify_password');
    const password = document.getElementsByName('password');
    var verify_password_data = verify_password[0].value
    var password_data = password[0].value

    console.log(verify_password_data);

    if (verify_password_data && password_data) {
        if (verify_password_data !== password_data) {
            const box = document.getElementById(`verify_password-box`)
            // const tagInput = document.getElementsByName(password)
            verify_password[0].className = 'form-control is-invalid'

            // Tạo thẻ div có các thuộc tính
            let create_div = create_valid_feedback("Mật khẩu xác nhận không hợp lệ.");
            if (!box.querySelector('.invalid-feedback'))
                box.insertBefore(create_div, box.children[-1])
        } else {
            const box = document.getElementById(`verify_password-box`)

            verify_password[0].className = 'form-control is-valid'

            // Tạo thẻ div có các thuộc tính
            let create_div = create_valid_feedback("valid", "OK")
            if (!box.querySelector('.valid-feedback'))
                box.insertBefore(create_div, box.children[-1])
        }
    } else {
        const feedback = document.getElementById("validationServerFeedback")
        feedback.style = "dislay: none;"

        verify_password[0].className = 'form-control'
    }
}

function checkEmpty(content) {
    if (content[0].value)
        return content[0].value

    let box = document.getElementById(`${content[0].name}-box`)
    const tagInput = document.getElementsByName(content[0].name)

    if (content[0].name == "first_name" || content[0].name == "last_name")
        box = document.getElementById(`full_name-box`)

    // Tạo thẻ div có các thuộc tính
    let create_div = create_valid_feedback("Nhập thông tin để xác thực.");

    tagInput[0].className = 'form-control is-invalid';

    if (!box.querySelector('.invalid-feedback'))
        box.insertBefore(create_div, box.children[-1]);

    return "";
}

function create_valid_feedback(className = "invalid", content) {
    let create_div = document.createElement('div');
    create_div.className = `${className}-feedback`;
    create_div.id = "validationServerFeedback";
    create_div.textContent = content;

    return create_div;
}

function otpCode_clickEnvent() {
    const code_input = document.getElementsByName("otp-code");
    const box = document.getElementById("verify_password-box");
    var code = code_input[0].value;

    document.getElementById('resend-otpcode').style = ''
    fetch(`{% url 'register' %}?otp_code={{user}} ${code}`, { method: "POST" })
        .then(response => {
            let data = response.json();
            if (response.status == 400) {
                let create_div = create_valid_feedback(data.message);

                if (!box.querySelector('.invalid-feedback'))
                    box.insertBefore(create_div, box.children[-1]);
            }
        });
}