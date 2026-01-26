/* --- Vynucení startu nahoře po obnovení stránky --- */
if (history.scrollRestoration) {
    history.scrollRestoration = 'manual'; // Vypne pamatování pozice
}

document.addEventListener('DOMContentLoaded', function() {
    
    // Pro jistotu ještě explicitní posun nahoru při načtení
    window.scrollTo(0, 0);

    // 1. Inicializace AOS (Animace)
    AOS.init({
        once: true,
        offset: 80,
        duration: 800,
        easing: 'ease-out-cubic',
    });

    // 2. Smooth Scroll pro odkazy (bez změny URL)
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                /* Najděte tento řádek a změňte číslo na 90 */
                const headerOffset = 90;
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.scrollY - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: "smooth"
                });
            }
        });
    });
    /* --- TESTIMONIALS CAROUSEL (MANUAL BUTTONS ONLY) --- */
    const track = document.querySelector('.testimonials-track');
    const cards = document.querySelectorAll('.testimonial-card');
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');
    
    if (track && cards.length > 0) {
        let currentIndex = 0;
        
        // Zjistíme, kolik karet se vejde na obrazovku (1 pro mobil, 2 pro desktop)
        const getItemsToShow = () => window.innerWidth > 992 ? 2 : 1;
        
        const updateCarousel = () => {
            const cardWidth = cards[0].offsetWidth;
            const gap = 30; // Mezera definovaná v CSS
            const moveAmount = (cardWidth + gap) * currentIndex;
            track.style.transform = `translateX(-${moveAmount}px)`;
        };

        // Kliknutí na "Další"
        nextBtn.addEventListener('click', () => {
            const itemsToShow = getItemsToShow();
            const maxIndex = cards.length - itemsToShow; 
            
            if (currentIndex < maxIndex) {
                currentIndex++;
            } else {
                currentIndex = 0; // Smyčka na začátek
            }
            updateCarousel();
        });

        // Kliknutí na "Předchozí"
        prevBtn.addEventListener('click', () => {
            const itemsToShow = getItemsToShow();
            const maxIndex = cards.length - itemsToShow;

            if (currentIndex > 0) {
                currentIndex--;
            } else {
                currentIndex = maxIndex; // Skok na konec
            }
            updateCarousel();
        });

        // Reset při změně velikosti okna
        window.addEventListener('resize', () => {
            currentIndex = 0;
            updateCarousel();
        });
    }
    /* --- CHYTRÝ FORMULÁŘ (Auto-fill) --- */
    const subjectCheckboxes = document.querySelectorAll('#subjectType input');
    const serviceCheckboxes = document.querySelectorAll('#serviceType input');
    const messageBox = document.getElementById('messageBox');

    // Funkce pro sestavení zprávy
    function updateMessage() {
        // 1. Získáme vybrané subjekty (Firma, OSVČ...)
        const selectedSubjects = Array.from(subjectCheckboxes)
            .filter(cb => cb.checked)
            .map(cb => cb.value);

        // 2. Získáme vybrané služby (Daně, Mzdy...)
        const selectedServices = Array.from(serviceCheckboxes)
            .filter(cb => cb.checked)
            .map(cb => cb.value);

        // 3. Sestavíme větu
        let text = "";

        if (selectedSubjects.length > 0) {
            // "Jsme Firma a OSVČ..."
            text += "Dobrý den, jsem/jsme " + selectedSubjects.join(" a ") + ". ";
        } else {
            text += "Dobrý den, ";
        }

        if (selectedServices.length > 0) {
            // "...a máme zájem o daně a mzdy."
            text += "Mám/e zájem o " + selectedServices.join(", ") + ".";
        }

        // 4. Vložíme do textarea
        // (Pouze pokud uživatel nezačal psát něco úplně vlastního, abychom mu to nepřepsali)
        // Ale pro jednoduchost to teď budeme aktualizovat, dokud do textarea neklikne.
        messageBox.value = text;
    }

    // Nasadíme posluchače na všechny checkboxy
    const allCheckboxes = [...subjectCheckboxes, ...serviceCheckboxes];
    allCheckboxes.forEach(cb => {
        cb.addEventListener('change', updateMessage);
    });
});