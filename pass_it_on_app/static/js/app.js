document.addEventListener("DOMContentLoaded", function () {
    /**
     * HomePage - Help section
     */
    class Help {
        constructor($el) {
            this.$el = $el;
            this.$buttonsContainer = $el.querySelector(".help--buttons");
            this.$slidesContainers = $el.querySelectorAll(".help--slides");
            this.init();
        }

        init() {
            this.updatePagination();
            this.events();
        }

        events() {
            /**
             * Slide buttons
             */
            this.$buttonsContainer.addEventListener("click", e => {
                if (e.target.classList.contains("btn")) {
                    this.changeSlide(e);
                }
            });

            /**
             * Pagination buttons
             */
            this.$el.addEventListener("click", e => {
                if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
                    this.changePage(e);
                }
            });
        }

        changeSlide(e) {
            e.preventDefault();
            const $btn = e.target;

            // Buttons Active class change
            [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
            $btn.classList.add("active");

            // Current slide
            this.currentSlide = $btn.parentElement.dataset.id;

            // Slides active class change
            this.$slidesContainers.forEach(el => {
                el.classList.remove("active");

                if (el.dataset.id === this.currentSlide) {
                    el.classList.add("active");
                }
                // Generate pagination for the current slide
                const itemsCount = el.querySelectorAll(".help--slides-items > li").length;
                this.generatePagination(itemsCount);
            });
            this.updatePagination()
        }

        generatePagination(itemsCount) {
            const totalPages = Math.ceil(itemsCount / ITEMS_PER_PAGE);

            // Only 1 page or no pages
            if (totalPages <= 1) {
                const existingPaginationContainer = document.querySelector(".help--slides-pagination");
                if (existingPaginationContainer) {
                    existingPaginationContainer.remove();
                }
                return;
            }

            const paginationContainer = document.createElement("ul");
            paginationContainer.classList.add("help--slides-pagination");

            for (let i = 1; i <= totalPages; i++) {
                const button = document.createElement("li");
                button.classList.add("btn", "btn--small", "btn--without-border");
                const link = document.createElement("a");
                link.href = "#help";
                link.textContent = i;
                link.dataset.page = i;

                if (i === 1) {
                    button.classList.add("active");
                    this.showItemsForPage(i);
                }

                button.appendChild(link);
                paginationContainer.appendChild(button);

            }
            paginationContainer.addEventListener("click", (e) => {
                if (e.target.tagName === "A") {
                    e.preventDefault();
                    const newPage = parseInt(e.target.dataset.page);
                    this.showItemsForPage(newPage);

                    [...paginationContainer.children].forEach(btn => btn.classList.remove("active"));
                    e.target.parentElement.classList.add("active");
                }
            });

            const existingPaginationContainer = this.$el.querySelector(".help--slides-pagination");
            if (existingPaginationContainer) {
                existingPaginationContainer.replaceWith(paginationContainer);
            } else {
                this.$el.appendChild(paginationContainer);
            }
        }

        updatePagination() {
            const activeSlide = this.$el.querySelector(".help--slides.active");
            if (activeSlide) {
                const itemsCount = activeSlide.querySelectorAll(".help--slides-items > li").length;
                this.generatePagination(itemsCount);
            }
        }

        showItemsForPage(pageNumber) {
            /**
             * Hide all
             */
            const allItems = document.querySelectorAll(".help--slides.active .help--slides-items > li");
            allItems.forEach(item => item.style.display = "none");

            const startIndex = (pageNumber - 1) * ITEMS_PER_PAGE;
            const endIndex = Math.min(startIndex + ITEMS_PER_PAGE, allItems.length);
            /**
             * Show current items
             */
            for (let i = startIndex; i < endIndex; i++) {
                allItems[i].style.display = "flex";
            }
        }

        changePage(e) {
            e.preventDefault();
            const page = e.target.dataset.page;
            console.log(page);
        }
    }

    const ITEMS_PER_PAGE = 5; // Number of items per page
    const helpSection = document.querySelector(".help");
    if (helpSection !== null) {
        new Help(helpSection);
    }

    /**
     * Form Select
     */
    class FormSelect {
        constructor($el) {
            this.$el = $el;
            this.options = [...$el.children];
            this.init();
        }

        init() {
            this.createElements();
            this.addEvents();
            this.$el.parentElement.removeChild(this.$el);
        }

        createElements() {
            // Input for value
            this.valueInput = document.createElement("input");
            this.valueInput.type = "text";
            this.valueInput.name = this.$el.name;

            // Dropdown container
            this.dropdown = document.createElement("div");
            this.dropdown.classList.add("dropdown");

            // List container
            this.ul = document.createElement("ul");

            // All list options
            this.options.forEach((el, i) => {
                const li = document.createElement("li");
                li.dataset.value = el.value;
                li.innerText = el.innerText;

                if (i === 0) {
                    // First clickable option
                    this.current = document.createElement("div");
                    this.current.innerText = el.innerText;
                    this.dropdown.appendChild(this.current);
                    this.valueInput.value = el.value;
                    li.classList.add("selected");
                }

                this.ul.appendChild(li);
            });

            this.dropdown.appendChild(this.ul);
            this.dropdown.appendChild(this.valueInput);
            this.$el.parentElement.appendChild(this.dropdown);
        }

        addEvents() {
            this.dropdown.addEventListener("click", e => {
                const target = e.target;
                this.dropdown.classList.toggle("selecting");

                // Save new value only when clicked on li
                if (target.tagName === "LI") {
                    this.valueInput.value = target.dataset.value;
                    this.current.innerText = target.innerText;
                }
            });
        }
    }

    document.querySelectorAll(".form-group--dropdown select").forEach(el => {
        new FormSelect(el);
    });

    /**
     * Hide elements when clicked on document
     */
    document.addEventListener("click", function (e) {
        const target = e.target;
        const tagName = target.tagName;

        if (target.classList.contains("dropdown")) return false;

        if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
            return false;
        }

        if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
            return false;
        }

        document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
            el.classList.remove("selecting");
        });
    });

    /**
     * Switching between form steps
     */
    class FormSteps {
        constructor(form) {
            this.$form = form;
            this.$next = form.querySelectorAll(".next-step");
            this.$prev = form.querySelectorAll(".prev-step");
            this.$step = form.querySelector(".form--steps-counter span");
            this.currentStep = 1;

            // items for filter
            this.$categoryCheckboxes = form.querySelectorAll(".category-checkbox");
            this.$allInstitutionsContainers = form.querySelectorAll(".institution-checkbox-container");

            // items from form

            this.$pickupQuantity = form.querySelector('[name="bags"]')
            // this.$selectedInstitution = form.querySelector('[name="organization"]:checked')

            this.$pickupStreet = form.querySelector('[name="address"]')
            this.$pickupCity = form.querySelector('[name="city"]')
            this.$pickupPostcode = form.querySelector('[name="postcode"]')
            this.$pickupPhone = form.querySelector('[name="phone"]')
            this.$pickupDate = form.querySelector('[name="data"]')
            this.$pickupTime = form.querySelector('[name="time"]')
            this.$pickupInfo = form.querySelector('[name="more_info"]')

            // summary items
            this.$summaryQuantity = form.querySelector("#summary-bags")
            this.$summaryCategories = form.querySelector("#summary-categories")
            this.$summaryInstitution = form.querySelector("#summary-institution")
            this.$summaryStreet = form.querySelector("#summary-street")
            this.$summaryCity = form.querySelector("#summary-city")
            this.$summaryPostcode = form.querySelector("#summary-postcode")
            this.$summaryPhone = form.querySelector("#summary-phone")
            this.$summaryDate = form.querySelector("#summary-date")
            this.$summaryTime = form.querySelector("#summary-time")
            this.$summaryInfo = form.querySelector("#summary-info")


            this.$errorMessage1 = form.querySelector("#error-message-1")
            this.$errorMessage2 = form.querySelector("#error-message-2")
            this.$errorMessage3 = form.querySelector("#error-message-3")
            this.$errorMessage4 = form.querySelector("#error-message-4")

            this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
            const $stepForms = form.querySelectorAll("form > div");
            this.slides = [...this.$stepInstructions, ...$stepForms];

            this.isButtonDisabled = false

            this.init();
        }

        /**
         * Init all methods
         */
        init() {
            this.events();
            this.updateForm();
        }

        /**
         * All events that are happening in form
         */
        events() {
            // Next step
            this.$next.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();

                    if (this.validateStep(this.currentStep)) {
                        this.currentStep++;
                        this.updateForm();
                    }
                });
            });

            // Next step button (validate on mouseover)
            this.$next.forEach(btn => {
                btn.addEventListener("mouseover", e => {
                    e.preventDefault();
                    if (!this.isButtonDisabled) {
                        const isValid = this.validateStep(this.currentStep);
                        if (isValid) {
                            btn.disabled = false;
                        } else {
                            btn.disabled = true;
                        }
                    }
                });
            });

            // Previous step
            this.$prev.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep--;
                    this.updateForm();
                });
            });

            // Category checkboxes change event
            this.$categoryCheckboxes.forEach(checkbox => {
                checkbox.addEventListener('click', () => {
                    this.updateForm(); // Trigger form update when categories change
                });
            });

            // Form submit
            // this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));

            this.$form.querySelector("form").addEventListener("submit", e => {
                e.preventDefault();
                this.submit(e);
            });

        }


        /**
         * Update form front-end
         * Show next or previous section etc.
         */
        updateForm() {

            // Reset previous error messages
            this.$errorMessage1.textContent
                = this.$errorMessage2.textContent
                = this.$errorMessage3.textContent
                = this.$errorMessage4.textContent
                = '';

            this.$step.innerText = this.currentStep;

            this.slides.forEach(slide => {
                slide.classList.remove("active");

                if (slide.dataset.step == this.currentStep) {
                    slide.classList.add("active");
                }
            });

            this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
            this.$step.parentElement.hidden = this.currentStep >= 6;

            // Filter institutions based on selected categories
            const selectedCategories = Array.from(this.$categoryCheckboxes)
                .filter(checkbox => checkbox.checked)
                .map(checkbox => checkbox.value);

            this.$allInstitutionsContainers.forEach(institutionContainer => {
                const institutionCategories = institutionContainer.dataset.categoryIds.split(',').map(category => parseInt(category.trim()));

                if (selectedCategories.every(category => institutionCategories.includes(parseInt(category)))) {
                    institutionContainer.style.display = "block";  // Show the institution
                } else {
                    institutionContainer.style.display = "none";   // Hide the institution
                }
            });

            // Summary display
            const selectedCategoriesNames = Array.from(this.$categoryCheckboxes)
                .filter(checkbox => checkbox.checked)
                .map(checkbox => checkbox.dataset.categoryName);

            this.$summaryQuantity.innerHTML = this.$pickupQuantity.value + " " + "worki" + "&nbsp;" // space
            const selectedInstitution = form.querySelector('[name="organization"]:checked')
            if (selectedInstitution) {
                this.$summaryInstitution.textContent = selectedInstitution.value
            }
            this.$summaryCategories.textContent = ("(" + selectedCategoriesNames + ")").replace(",", ", ")
            this.$summaryStreet.textContent = this.$pickupStreet.value
            this.$summaryCity.textContent = this.$pickupCity.value
            this.$summaryPostcode.textContent = this.$pickupPostcode.value
            this.$summaryPhone.textContent = this.$pickupPhone.value
            this.$summaryDate.textContent = this.$pickupDate.value
            this.$summaryTime.textContent = "godz. " + this.$pickupTime.value
            if (this.$pickupInfo.value === "") {
                this.$summaryInfo.textContent = "Brak uwag"
            } else {
                this.$summaryInfo.textContent = this.$pickupInfo.value
            }
            // Dynamically set the 'min' attribute for the date input

            const today = new Date().toISOString().split('T')[0];
            this.$pickupDate.setAttribute("min", today);
        }

        /**
         * Validate input fields for a specific step
         */
        validateStep(step) {
            switch (step) {
                case 1:
                    const selectedCategories = Array.from(this.$categoryCheckboxes).some(checkbox => checkbox.checked);
                    if (!selectedCategories) {
                        this.$errorMessage1.textContent = 'Zaznacz co najmniej jedną kategorię';
                        return false;
                    }
                    return true;
                case 2:
                    const numberOfBags = this.$pickupQuantity.value;
                    if (!numberOfBags || numberOfBags < 1) {
                        this.$errorMessage2.textContent = 'Podaj liczbę worków';
                        return false;
                    }
                    return true;
                case 3:
                    const selectedInstitution = form.querySelector('[name="organization"]:checked')
                    if (!selectedInstitution) {
                        this.$errorMessage3.textContent = 'Wybierz instytucję';
                        return false;
                    }
                    return true;
                case 4:
                    if (this.$pickupStreet.value === "") {
                        this.$errorMessage4.textContent = "Podaj nazwę ulicy";
                        return false;
                    }
                    if (this.$pickupCity.value === "") {
                        this.$errorMessage4.textContent = "Podaj nazwę miasta";
                        return false;
                    }
                    if (this.$pickupPostcode.value === "") {
                        this.$errorMessage4.textContent = "Podaj poprawny kod pocztowy";
                        return false;
                    }
                    if (this.$pickupPhone.value === "" ||
                        this.$pickupPhone.value.length > 15 ||
                        this.$pickupPhone.value.length < 9) {
                        this.$errorMessage4.textContent = "Podaj numer telefonu";
                        return false;
                    }
                    if (this.$pickupDate.value === "") {
                        this.$errorMessage4.textContent = "Podaj datę odbioru";
                        return false;
                    }
                    if (this.$pickupTime.value === "") {
                        this.$errorMessage4.textContent = "Podaj godzinę";
                        return false;
                    }
                    return true;

                default:
                    return true; // No validation for other steps by default
            }
        }

        /**
         * Submit form
         */
        submit(e) {
            e.preventDefault();
            const formElement = this.$form.querySelector("form");
            formElement.submit();
        }
    }

    const form = document.querySelector(".form--steps");
    if (form !== null) {
        new FormSteps(form);
    }
});
