function check_Password() {
    const password = document.getElementsByName("password")[0];
    const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$/;
    console.log(password.value);

    if (regex.test(password.value))
        password.className = "form-control is-valid";
    else if (!password.value) // input rỗng trả về bình thường
        password.className = "form-control";
    else
        password.className = "form-control is-invalid";
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

function show_password() {
    ["password", "verify_password"].forEach(password_tag => {
        const tag = document.getElementsByName(password_tag)[0];
        if (tag.type === "password") {
            tag.type = "text";
        } else {
            tag.type = "password";
        }
    })
}