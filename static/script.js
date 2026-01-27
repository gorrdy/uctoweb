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

    if (mainForm && popup) {
        mainForm.addEventListener('submit', function(e) {
            e.preventDefault(); 

            // 1. Zobrazit Popup
            popup.classList.add('active');
            
            // 2. Odpočet 1 sekunda
            setTimeout(() => {
                // 3. Změna na úspěch
                popupContent.classList.add('success-state');
                popupText.textContent = "Poptávka odeslána!";
                popupSubtext.textContent = "Přesměrovávám na potvrzení...";
                
                // 4. Skutečné odeslání formuláře
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
});