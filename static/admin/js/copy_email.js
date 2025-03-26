document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".copy-email-btn").forEach(button => {
        button.addEventListener("click", function () {
            const email = this.getAttribute("data-email");
            navigator.clipboard.writeText(email).then(() => {
                alert("Email скопирован: " + email);
            }).catch(err => {
                console.error("Ошибка копирования: ", err);
            });
        });
    });
});
