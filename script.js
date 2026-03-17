// =====================================================
// PORTFOLIO WEBSITE - JAVASCRIPT FUNCTIONALITY
// =====================================================

// Smooth Scrolling for Navigation Links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            targetElement.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
            
            // Close mobile menu if open
            const navbarCollapse = document.querySelector('.navbar-collapse');
            if (navbarCollapse.classList.contains('show')) {
                const toggler = document.querySelector('.navbar-toggler');
                toggler.click();
            }
        }
    });
});

// =====================================================
// CONTACT FORM VALIDATION
// =====================================================
const contactForm = document.getElementById('contactForm');

if (contactForm) {
    contactForm.addEventListener('submit', function (e) {
        e.preventDefault();
        
        // Get form values
        const name = document.getElementById('name').value.trim();
        const email = document.getElementById('email').value.trim();
        const subject = document.getElementById('subject').value.trim();
        const message = document.getElementById('message').value.trim();
        
        // Reset error messages
        clearErrorMessages();
        
        // Validation
        let isValid = true;
        
        if (name === '') {
            showError('nameError');
            isValid = false;
        }
        
        if (email === '') {
            showError('emailError');
            isValid = false;
        } else if (!isValidEmail(email)) {
            document.getElementById('emailError').textContent = 'Please enter a valid email address';
            showError('emailError');
            isValid = false;
        }
        
        if (subject === '') {
            showError('subjectError');
            isValid = false;
        }
        
        if (message === '') {
            showError('messageError');
            isValid = false;
        }
        
        // If all valid, show success message and reset form
        if (isValid) {
            showFormMessage('Thank you! Your message has been sent successfully. I will get back to you soon!', 'success');
            contactForm.reset();
            
            // Optional: Clear success message after 5 seconds
            setTimeout(() => {
                const formMessage = document.getElementById('formMessage');
                if (formMessage) {
                    formMessage.classList.add('d-none');
                }
            }, 5000);
        }
    });
}

// Helper function to validate email
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Helper function to show error
function showError(errorId) {
    const errorElement = document.getElementById(errorId);
    if (errorElement) {
        errorElement.classList.remove('d-none');
    }
}

// Helper function to clear all error messages
function clearErrorMessages() {
    const errorElements = document.querySelectorAll('[id$="Error"]');
    errorElements.forEach(element => {
        element.classList.add('d-none');
    });
}

// Helper function to show form message
function showFormMessage(message, type) {
    const formMessage = document.getElementById('formMessage');
    if (formMessage) {
        formMessage.textContent = message;
        formMessage.classList.remove('d-none', 'success', 'error');
        formMessage.classList.add(type);
        formMessage.style.display = 'block';
    }
}

// =====================================================
// FORM INPUT REAL-TIME VALIDATION
// =====================================================
const nameInput = document.getElementById('name');
const emailInput = document.getElementById('email');
const subjectInput = document.getElementById('subject');
const messageInput = document.getElementById('message');

if (nameInput) {
    nameInput.addEventListener('blur', function () {
        if (this.value.trim() === '') {
            document.getElementById('name').classList.add('is-invalid');
            document.getElementById('nameError').classList.remove('d-none');
        } else {
            document.getElementById('name').classList.remove('is-invalid');
            document.getElementById('nameError').classList.add('d-none');
        }
    });
}

if (emailInput) {
    emailInput.addEventListener('blur', function () {
        if (this.value.trim() === '' || !isValidEmail(this.value)) {
            document.getElementById('email').classList.add('is-invalid');
            document.getElementById('emailError').classList.remove('d-none');
        } else {
            document.getElementById('email').classList.remove('is-invalid');
            document.getElementById('emailError').classList.add('d-none');
        }
    });
}

if (subjectInput) {
    subjectInput.addEventListener('blur', function () {
        if (this.value.trim() === '') {
            document.getElementById('subject').classList.add('is-invalid');
            document.getElementById('subjectError').classList.remove('d-none');
        } else {
            document.getElementById('subject').classList.remove('is-invalid');
            document.getElementById('subjectError').classList.add('d-none');
        }
    });
}

if (messageInput) {
    messageInput.addEventListener('blur', function () {
        if (this.value.trim() === '') {
            document.getElementById('message').classList.add('is-invalid');
            document.getElementById('messageError').classList.remove('d-none');
        } else {
            document.getElementById('message').classList.remove('is-invalid');
            document.getElementById('messageError').classList.add('d-none');
        }
    });
}

// =====================================================
// ACTIVE NAVBAR LINK HIGHLIGHTING
// =====================================================
window.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    let currentSection = '';
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop - 100;
        if (window.scrollY >= sectionTop) {
            currentSection = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href').slice(1) === currentSection) {
            link.classList.add('active');
        }
    });
});

// =====================================================
// SCROLL ANIMATIONS FOR ELEMENTS
// =====================================================
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver(function (entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'fadeIn 0.8s ease-out forwards';
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe all cards for scroll animation
document.querySelectorAll('.skill-card, .project-card, .education-card, .experience-card, .contact-info-card').forEach(card => {
    observer.observe(card);
});

// =====================================================
// MOBILE MENU AUTO-CLOSE ON LINK CLICK
// =====================================================
const navbarLinks = document.querySelectorAll('.navbar-nav a');
const navbarToggler = document.querySelector('.navbar-toggler');

navbarLinks.forEach(link => {
    link.addEventListener('click', () => {
        if (navbarToggler.offsetParent !== null) { // Check if toggler is visible (mobile)
            navbarToggler.click();
        }
    });
});

// =====================================================
// ADD ACTIVE CLASS TO CURRENT NAV LINK
// ===================================================== 
document.querySelectorAll('.navbar-nav a').forEach(link => {
    link.addEventListener('click', function () {
        document.querySelectorAll('.navbar-nav a').forEach(l => l.classList.remove('active'));
        this.classList.add('active');
    });
});

// =====================================================
// BUTTON HOVER EFFECTS
// ===================================================== 
const buttons = document.querySelectorAll('.btn');
buttons.forEach(button => {
    button.addEventListener('mouseenter', function () {
        this.style.transform = 'translateY(-2px)';
    });
    
    button.addEventListener('mouseleave', function () {
        this.style.transform = 'translateY(0)';
    });
});

// =====================================================
// CONSOLE WELCOME MESSAGE
// ===================================================== 
console.log('%c Welcome to Ingabire Kalinda Irene\'s Portfolio! ', 'background: #0d6efd; color: white; font-size: 14px; padding: 10px;');
console.log('%c Software Developer Student | BTEC IT Level 3 Extended Diploma ', 'background: #0dcaf0; color: #333; font-size: 12px; padding: 5px;');
console.log('Thank you for visiting! Feel free to explore and connect with me.');
