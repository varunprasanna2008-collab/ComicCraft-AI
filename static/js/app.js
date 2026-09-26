document.addEventListener(
    "DOMContentLoaded",
    function () {

        const form =
            document.getElementById(
                "comicForm"
            );

        const button =
            document.getElementById(
                "generateButton"
            );

        const loading =
            document.getElementById(
                "loadingMessage"
            );


        if (!form) {
            return;
        }


        form.addEventListener(
            "submit",
            function () {

                if (button) {

                    button.disabled =
                        true;

                    button.innerText =
                        "✨ Creating Comic...";
                }


                if (loading) {

                    loading.style.display =
                        "block";
                }

            }
        );

    }
);