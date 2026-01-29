/* --- Vynucení startu nahoře po obnovení stránky --- */
if (history.scrollRestoration) {
    history.scrollRestoration = 'manual';
}

document.addEventListener('DOMContentLoaded', function() {
    
    window.scrollTo(0, 0);

    // 1. Inicializace AOS
    if (typeof AOS !== 'undefined') {
        AOS.init({
            once: true, offset: 80, duration: 800, easing: 'ease-out-cubic',
        });
    }

    // 2. Smooth Scroll
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                const headerOffset = 90;
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.scrollY - headerOffset;
                window.scrollTo({ top: offsetPosition, behavior: "smooth" });
            }
        });
    });

    /* --- LOGIKA ODPOČTU PŘESMĚROVÁNÍ (Thank You Page) --- */
    const countdownEl = document.getElementById('countdown');
    const redirectBar = document.getElementById('redirectBar');

    if (countdownEl && redirectBar) {
        let timeLeft = 15;
        const totalTime = 15;

        const timer = setInterval(() => {
            timeLeft--;
            
            // Aktualizace textu
            countdownEl.textContent = timeLeft;
            
            // Aktualizace šířky progress baru
            const percentage = (timeLeft / totalTime) * 100;
            redirectBar.style.width = percentage + "%";

            // Přesměrování po uplynutí času
            if (timeLeft <= 0) {
                clearInterval(timer);
                window.location.href = "/"; // Návrat na hlavní stránku
            }
        }, 1000);
    }

    /* --- FORMULÁŘ POPUP LOGIKA --- */
    const mainForm = document.getElementById('mainForm');
    const popup = document.getElementById('submissionPopup');
    const popupText = document.getElementById('popupText');
    const popupSubtext = document.getElementById('popupSubtext');
    const popupContent = document.querySelector('.popup-content');

    /* Najděte v script.js sekci LOGIKA FORMULÁŘE a nahraďte ji tímto komplexním řešením */

    if (mainForm && popup) {
        const emailField = document.getElementById('emailInput');
        const phoneField = document.getElementById('phoneInput');
        const errorMsg = document.getElementById('contactError');

        // Funkce pro vyčištění a formátování čísla
        function validateAndFormatPhone(value) {
            // 1. Odstraníme vše kromě číslic a úvodního plusu
            let cleaned = value.replace(/[^\d+]/g, '');
            
            // 2. Pokud začíná 00, převedeme na +
            if (cleaned.startsWith('00')) {
                cleaned = '+' + cleaned.substring(2);
            }

            // 3. Logika předvoleb
            if (cleaned.length === 9 && !cleaned.startsWith('+')) {
                // Máme 9 číslic bez předvolby -> automaticky +420
                cleaned = '+420' + cleaned;
            }

            // 4. Základní validace délky (mezinárodní formát má obvykle 11-15 znaků vč. +)
            if (cleaned.length < 12 || !cleaned.startsWith('+')) {
                return { isValid: false, value: cleaned };
            }

            // 5. Formátování pro oko: +XXX YYY YYY YYY...
            const prefix = cleaned.substring(0, 4); // +420, +421 atd.
            const rest = cleaned.substring(4);
            const chunks = rest.match(/.{1,3}/g); // Rozdělit po 3 číslicích
            const formatted = prefix + ' ' + chunks.join(' ');

            return { isValid: true, value: formatted };
        }

        // Volitelné: Formátování "za běhu", když uživatel opustí pole (blur)
        phoneField.addEventListener('blur', function() {
            if (this.value.trim() !== "") {
                const result = validateAndFormatPhone(this.value);
                this.value = result.value;
            }
        });

        mainForm.addEventListener('submit', function(e) {
            e.preventDefault(); 

            const email = emailField.value.trim();
            const phoneRaw = phoneField.value.trim();
            
            // Reset chyb
            emailField.classList.remove('input-error');
            phoneField.classList.remove('input-error');
            errorMsg.style.display = 'none';

            // A) Kontrola prázdnoty (musí být aspoň jeden kontakt)
            if (!email && !phoneRaw) {
                errorMsg.textContent = "Vyplňte prosím e-mail nebo telefon, abychom se vám mohli ozvat.";
                errorMsg.style.display = 'block';
                emailField.classList.add('input-error');
                phoneField.classList.add('input-error');
                return;
            }

            // B) Pokud je zadán telefon, zvalidujeme jeho formát
            if (phoneRaw !== "") {
                const phoneResult = validateAndFormatPhone(phoneRaw);
                if (!phoneResult.isValid) {
                    errorMsg.textContent = "Telefonní číslo nemá správný formát (chybí předvolba nebo je příliš krátké).";
                    errorMsg.style.display = 'block';
                    phoneField.classList.add('input-error');
                    return;
                }
                // Uložíme vyčištěné a naformátované číslo zpět do pole před odesláním
                phoneField.value = phoneResult.value;
            }

            // Pokud vše projde, spustíme animaci úspěchu
            popup.classList.add('active');
            
            setTimeout(() => {
                popupContent.classList.add('success-state');
                document.getElementById('popupText').textContent = "Poptávka odeslána!";
                document.getElementById('popupSubtext').textContent = "Přesměrovávám na potvrzení...";
                
                setTimeout(() => {
                    mainForm.submit(); 
                }, 800); 
            }, 1000); 
        });
    }

    /* --- TESTIMONIALS CAROUSEL --- */
    const track = document.querySelector('.testimonials-track');
    const cards = document.querySelectorAll('.testimonial-card');
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');
    
    if (track && cards.length > 0) {
        let currentIndex = 0;
        const getItemsToShow = () => window.innerWidth > 992 ? 2 : 1;
        const updateCarousel = () => {
            const cardWidth = cards[0].offsetWidth;
            const gap = 30;
            const moveAmount = (cardWidth + gap) * currentIndex;
            track.style.transform = `translateX(-${moveAmount}px)`;
        };

        nextBtn.addEventListener('click', () => {
            const itemsToShow = getItemsToShow();
            const maxIndex = cards.length - itemsToShow; 
            if (currentIndex < maxIndex) currentIndex++;
            else currentIndex = 0;
            updateCarousel();
        });

        prevBtn.addEventListener('click', () => {
            const itemsToShow = getItemsToShow();
            const maxIndex = cards.length - itemsToShow;
            if (currentIndex > 0) currentIndex--;
            else currentIndex = maxIndex;
            updateCarousel();
        });

        window.addEventListener('resize', () => {
            currentIndex = 0;
            updateCarousel();
        });
    }

    /* --- CHYTRÝ FORMULÁŘ --- */
    const subjectCheckboxes = document.querySelectorAll('#subjectType input');
    const serviceCheckboxes = document.querySelectorAll('#serviceType input');
    const messageBox = document.getElementById('messageBox');

    if (messageBox) {
        function updateMessage() {
            const selectedSubjects = Array.from(subjectCheckboxes).filter(cb => cb.checked).map(cb => cb.value);
            const selectedServices = Array.from(serviceCheckboxes).filter(cb => cb.checked).map(cb => cb.value);
            let text = "";
            if (selectedSubjects.length > 0) text += "Dobrý den, jsem/jsme " + selectedSubjects.join(" a ") + ". ";
            else text += "Dobrý den, ";
            if (selectedServices.length > 0) text += "Mám/e zájem o " + selectedServices.join(", ") + ".";
            messageBox.value = text;
        }

        const allCheckboxes = [...subjectCheckboxes, ...serviceCheckboxes];
        allCheckboxes.forEach(cb => {
            cb.addEventListener('change', updateMessage);
        });
    }
    /* --- MOBILNÍ MENU LOGIKA --- */
    const hamburger = document.querySelector('.hamburger');
    const mobileNav = document.querySelector('.mobile-nav-overlay');
    const mobileLinks = document.querySelectorAll('.mobile-nav-links a');

    if (hamburger && mobileNav) {
        // Toggle menu při kliknutí na hamburger
        hamburger.addEventListener('click', function() {
            this.classList.toggle('active');
            mobileNav.classList.toggle('active');
            
            // Zamezení scrollování pozadí
            if (mobileNav.classList.contains('active')) {
                document.body.style.overflow = 'hidden';
            } else {
                document.body.style.overflow = '';
            }
        });

        // Zavření menu po kliknutí na odkaz
        mobileLinks.forEach(link => {
            link.addEventListener('click', () => {
                hamburger.classList.remove('active');
                mobileNav.classList.remove('active');
                document.body.style.overflow = '';
            });
        });
    }
});