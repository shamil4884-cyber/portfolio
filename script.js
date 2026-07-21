document.addEventListener("DOMContentLoaded", () => {
    
    // ==========================================
    // 1. DOM Elements & State Setup
    // ==========================================
    const htmlElement = document.documentElement;
    const navbar = document.getElementById("navbar");
    const navMenu = document.getElementById("nav-menu");
    const hamburger = document.getElementById("hamburger");
    const navLinks = document.querySelectorAll(".nav-link");
    
    const themeToggleBtn = document.getElementById("theme-toggle");
    const themeIcon = document.getElementById("theme-icon");
    
    const profileCard = document.getElementById("profile-card");
    const profileGlow = profileCard ? profileCard.querySelector(".tilt-card-glow") : null;
    
    const typedTextElement = document.getElementById("typed-text");
    
    const blob1 = document.getElementById("blob-1");
    const blob2 = document.getElementById("blob-2");
    const blob3 = document.getElementById("blob-3");
    
    // ==========================================
    // 2. Persistent Theme Sync Engine
    // ==========================================
    const savedTheme = localStorage.getItem("portfolio-theme") || "light";
    htmlElement.setAttribute("data-theme", savedTheme);
    syncIconStyle(savedTheme);

    themeToggleBtn.addEventListener("click", () => {
        const activeTheme = htmlElement.getAttribute("data-theme");
        const alternateTheme = activeTheme === "dark" ? "light" : "dark";
        
        htmlElement.setAttribute("data-theme", alternateTheme);
        localStorage.setItem("portfolio-theme", alternateTheme);
        syncIconStyle(alternateTheme);
    });

    function syncIconStyle(themeState) {
        if (themeState === "dark") {
            themeIcon.className = "fas fa-sun";
        } else {
            themeIcon.className = "fas fa-moon";
        }
    }

    // ==========================================
    // 3. Responsive Navigation Menu
    // ==========================================
    hamburger.addEventListener("click", () => {
        navMenu.classList.toggle("active");
        hamburger.classList.toggle("open");
    });

    // Close menu when clicking a link
    navLinks.forEach(link => {
        link.addEventListener("click", () => {
            navMenu.classList.remove("active");
            hamburger.classList.remove("open");
        });
    });

    // Collapse Navigation on Scroll
    window.addEventListener("scroll", () => {
        if (window.scrollY > 50) {
            navbar.classList.add("scrolled");
        } else {
            navbar.classList.remove("scrolled");
        }
        highlightActiveSection();
    });

    // Active Section Tracking
    const sections = document.querySelectorAll("section, header");
    function highlightActiveSection() {
        let scrollPosition = window.scrollY + 100;
        
        sections.forEach(section => {
            const top = section.offsetTop;
            const height = section.offsetHeight;
            const id = section.getAttribute("id");
            
            if (scrollPosition >= top && scrollPosition < top + height) {
                navLinks.forEach(link => {
                    link.classList.remove("active");
                    if (link.getAttribute("href") === `#${id}`) {
                        link.classList.add("active");
                    }
                });
            }
        });
    }

    // ==========================================
    // 4. 3D Tilt Profile Card Effect
    // ==========================================
    if (profileCard) {
        profileCard.addEventListener("mousemove", (e) => {
            const cardRect = profileCard.getBoundingClientRect();
            
            // Mouse coordinates relative to card center
            const mouseX = e.clientX - cardRect.left - cardRect.width / 2;
            const mouseY = e.clientY - cardRect.top - cardRect.height / 2;
            
            // Convert to tilt degrees (max 15 deg)
            const rotateY = (mouseX / (cardRect.width / 2)) * 12;
            const rotateX = -(mouseY / (cardRect.height / 2)) * 12;
            
            profileCard.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
            
            // Light reflectivity glare effect
            if (profileGlow) {
                const glowX = ((e.clientX - cardRect.left) / cardRect.width) * 100;
                const glowY = ((e.clientY - cardRect.top) / cardRect.height) * 100;
                profileGlow.style.background = `radial-gradient(circle at ${glowX}% ${glowY}%, var(--card-glow), transparent 70%)`;
                profileGlow.style.opacity = "0.8";
            }
        });
        
        profileCard.addEventListener("mouseleave", () => {
            profileCard.style.transform = "rotateX(0deg) rotateY(0deg)";
            if (profileGlow) {
                profileGlow.style.opacity = "0.25";
                profileGlow.style.background = "var(--accent-gradient)";
            }
        });
    }

    // ==========================================
    // 5. Mouse Follow Background Glow Blobs
    // ==========================================
    let targetX = 0, targetY = 0;
    let currentX1 = 0, currentY1 = 0;
    let currentX2 = 0, currentY2 = 0;
    
    window.addEventListener("mousemove", (e) => {
        targetX = e.clientX;
        targetY = e.clientY;
    });

    function animateBlobs() {
        // Interpolate position for smooth lag effect
        currentX1 += (targetX - currentX1 - 200) * 0.05;
        currentY1 += (targetY - currentY1 - 200) * 0.05;
        
        currentX2 += (targetX - currentX2 - 250) * 0.02;
        currentY2 += (targetY - currentY2 - 250) * 0.02;

        if (blob1) {
            blob1.style.transform = `translate3d(${currentX1}px, ${currentY1}px, 0)`;
        }
        if (blob2) {
            blob2.style.transform = `translate3d(${currentX2}px, ${currentY2}px, 0)`;
        }
        
        requestAnimationFrame(animateBlobs);
    }
    animateBlobs();

    // ==========================================
    // 6. Typist Subtitle Carousel
    // ==========================================
    if (typedTextElement) {
        const words = ["Full Stack Developer", "BCA Graduate", "Python / Django Expert", "Flutter Developer", "Systems Programmer"];
        let wordIndex = 0;
        let charIndex = 0;
        let isDeleting = false;
        let typingSpeed = 100;

        function type() {
            const currentWord = words[wordIndex];
            
            if (isDeleting) {
                charIndex--;
                typingSpeed = 50; // speed up backspacing
            } else {
                charIndex++;
                typingSpeed = 100; // default typing speed
            }

            typedTextElement.textContent = currentWord.substring(0, charIndex);

            // Determine state transitions
            if (!isDeleting && charIndex === currentWord.length) {
                isDeleting = true;
                typingSpeed = 1500; // Pause at end of word
            } else if (isDeleting && charIndex === 0) {
                isDeleting = false;
                wordIndex = (wordIndex + 1) % words.length;
                typingSpeed = 500; // Pause before typing next word
            }

            setTimeout(type, typingSpeed);
        }
        
        // Start typist loop
        setTimeout(type, 1000);
    }

    // ==========================================
    // 7. Interactive Smart Parking Simulator
    // ==========================================
    const parkingGrid = document.getElementById("parking-grid");
    const availableSlotsCount = document.getElementById("available-slots-count");
    const reservedSlotsCount = document.getElementById("reserved-slots-count");
    const receiptBox = document.getElementById("sim-receipt-box");
    const resetSimBtn = document.getElementById("reset-sim");

    // Initialize mock database state
    const initialSlots = [
    { id: "A1", reserved: false, type: "VIP" },
    { id: "A2", reserved: false, type: "Standard" },
    { id: "A3", reserved: false, type: "EV Charging" },
    { id: "A4", reserved: false, type: "Standard" },
    { id: "B1", reserved: false, type: "Standard" },
    { id: "B2", reserved: false, type: "EV Charging" },
    { id: "B3", reserved: false, type: "Standard" },
    { id: "B4", reserved: false, type: "VIP" }
];

    let currentSlots = JSON.parse(JSON.stringify(initialSlots));

    function renderParkingLot() {
        if (!parkingGrid) return;
        
        parkingGrid.innerHTML = "";
        let availableCount = 0;
        let reservedCount = 0;

        currentSlots.forEach(slot => {
            if (slot.reserved) {
                reservedCount++;
            } else {
                availableCount++;
            }

            const slotEl = document.createElement("div");
            slotEl.className = `parking-slot ${slot.reserved ? 'reserved' : 'available'}`;
            slotEl.setAttribute("data-id", slot.id);
            slotEl.setAttribute("title", `${slot.type} Spot - Click to reserve`);

            slotEl.innerHTML = `
                <span class="slot-name">${slot.id}</span>
                <i class="fas ${slot.reserved ? 'fa-car' : 'fa-check'}"></i>
                <span class="slot-status">${slot.reserved ? 'Reserved' : 'Open'}</span>
            `;

            slotEl.addEventListener("click", () => handleSlotClick(slot));
            parkingGrid.appendChild(slotEl);
        });

        // Update counts in HTML
        if (availableSlotsCount) availableSlotsCount.textContent = availableCount;
        if (reservedSlotsCount) reservedSlotsCount.textContent = reservedCount;
    }

    function handleSlotClick(slot) {
        if (slot.reserved) {
            receiptBox.innerHTML = `
                <div class="receipt-inner" style="border-color: var(--red-status);">
                    <p class="receipt-msg" style="color: var(--red-status);">
                        <i class="fas fa-times-circle"></i> Slot ${slot.id} is already occupied! Please select an open green slot.
                    </p>
                </div>
            `;
            return;
        }

        // Reserve slot
        slot.reserved = true;
        renderParkingLot();

        // Booking ID simulation
        const bookingId = "PK-" + Math.floor(1000 + Math.random() * 9000);
        
        receiptBox.innerHTML = `
            <div class="receipt-inner" style="border-color: var(--green-status); animation: pulse 1s 1;">
                <p class="receipt-msg" style="color: var(--green-status); font-weight: 700;">
                    <i class="fas fa-check-double"></i> Slot ${slot.id} Reserved Successfully!
                </p>
                <p style="font-size: 12px; margin-top: 4px;">
                    Type: <strong>${slot.type}</strong> | Ticket ID: <code style="background: var(--border-color); padding: 2px 6px; border-radius: 4px;">${bookingId}</code>
                </p>
            </div>
        `;

        // Confetti Celebration
        if (typeof confetti === "function") {
            confetti({
                particleCount: 80,
                spread: 60,
                origin: { y: 0.8 }
            });
        }
    }

    if (resetSimBtn) {
        resetSimBtn.addEventListener("click", () => {
            currentSlots = JSON.parse(JSON.stringify(initialSlots));
            renderParkingLot();
            receiptBox.innerHTML = `
                <div class="receipt-inner">
                    <p class="receipt-msg"><i class="fas fa-check-circle"></i> Slots reset! Click any green slot to reserve.</p>
                </div>
            `;
        });
    }

    // Initialize Simulator
    renderParkingLot();

    // ==========================================
    // 8. Contact Form Handler & Mock Mailer
    // ==========================================
    const contactForm = document.getElementById("contact-form");
    const submitBtn = document.getElementById("form-submit-btn");
    const feedbackMsg = document.getElementById("form-feedback");

    if (contactForm) {
        contactForm.addEventListener("submit", (e) => {
            e.preventDefault();

            const name = document.getElementById("contact-name").value;
            const email = document.getElementById("contact-email").value;
            const subject = document.getElementById("contact-subject").value;
            const message = document.getElementById("contact-message").value;

            if (!name || !email || !subject || !message) {
                showFeedback("Please fill out all fields.", "error");
                return;
            }

            // Enter loading state
            submitBtn.disabled = true;
            submitBtn.querySelector(".btn-text").classList.add("hidden");
            submitBtn.querySelector(".spinner").classList.remove("hidden");
            feedbackMsg.classList.add("hidden");

            // Attempt to send to local python backend database
            fetch("http://localhost:8000/api/messages", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    name: name,
                    email: email,
                    subject: subject,
                    message: message
                })
            })
            .then(res => {
                if (!res.ok) throw new Error("Server error");
                return res.json();
            })
            .then(data => {
                submitBtn.disabled = false;
                submitBtn.querySelector(".btn-text").classList.remove("hidden");
                submitBtn.querySelector(".spinner").classList.add("hidden");
                
                showFeedback(`Thank you, ${name}! Your message was saved to the database.`, "success");
                contactForm.reset();
                triggerConfetti();
            })
            .catch(err => {
                // FALLBACK: Local simulation mode when database server is offline
                console.warn("Backend server not running. Falling back to simulation mode.");
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.querySelector(".btn-text").classList.remove("hidden");
                    submitBtn.querySelector(".spinner").classList.add("hidden");

                    showFeedback(`Thank you, ${name}! Your message was received (Simulation Mode: Server Offline).`, "success");
                    contactForm.reset();
                    triggerConfetti();
                }, 1000);
            });
        });
    }

    function triggerConfetti() {
        if (typeof confetti === "function") {
            confetti({
                particleCount: 100,
                spread: 70,
                origin: { y: 0.6 }
            });
        }
    }

    function showFeedback(msg, type) {
        if (!feedbackMsg) return;
        feedbackMsg.textContent = msg;
        feedbackMsg.className = `form-feedback-message ${type}`;
        feedbackMsg.classList.remove("hidden");
    }

    // ==========================================
    // 9. ScrollReveal Engine Setup
    // ==========================================
    if (typeof ScrollReveal !== 'undefined') {
        const isMobile = window.innerWidth < 768;

        const revealConfig = {
            origin: 'bottom',
            distance: isMobile ? '20px' : '40px', 
            duration: 1000,
            delay: 100,
            opacity: 0,
            reset: false,
            useDelay: 'onload'
        };

        ScrollReveal().reveal('.reveal-bottom', revealConfig);
        ScrollReveal().reveal('.reveal-left', {
            ...revealConfig,
            origin: 'left',
            distance: isMobile ? '20px' : '50px'
        });
        ScrollReveal().reveal('.reveal-right', {
            ...revealConfig,
            origin: 'right',
            distance: isMobile ? '20px' : '50px'
        });
        ScrollReveal().reveal('.reveal-card', {
            ...revealConfig,
            interval: 100
        });
    }
});