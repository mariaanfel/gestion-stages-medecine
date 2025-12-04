// static/js/sidebar.js
document.addEventListener('DOMContentLoaded', function() {
    const mobileToggle = document.getElementById('mobileToggle');
    const sidebar = document.getElementById('sidebar');
    
    // Ajouter l'attribut data-role à l'avatar
    const avatar = document.querySelector('.avatar');
    if (avatar) {
        const role = document.querySelector('.user-role').textContent.toLowerCase();
        if (role.includes('étudiant')) avatar.setAttribute('data-role', 'student');
        else if (role.includes('médecin')) avatar.setAttribute('data-role', 'doctor');
        else if (role.includes('chef')) avatar.setAttribute('data-role', 'chef');
        else if (role.includes('responsable')) avatar.setAttribute('data-role', 'responsable');
        else if (role.includes('administrateur')) avatar.setAttribute('data-role', 'admin');
    }
    
    // Gestion du responsive
    function checkScreenSize() {
        if (window.innerWidth <= 768) {
            if (mobileToggle) mobileToggle.style.display = 'flex';
            if (sidebar) sidebar.classList.remove('open');
        } else {
            if (mobileToggle) mobileToggle.style.display = 'none';
            if (sidebar) sidebar.classList.add('open');
        }
    }
    
    // Initialiser
    checkScreenSize();
    window.addEventListener('resize', checkScreenSize);
    
    // Toggle sidebar sur mobile
    if (mobileToggle) {
        mobileToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            sidebar.classList.toggle('open');
        });
    }
    
    // Fermer sidebar en cliquant à l'extérieur (mobile)
    document.addEventListener('click', function(event) {
        if (window.innerWidth <= 768 && 
            sidebar && 
            !sidebar.contains(event.target) && 
            (!mobileToggle || !mobileToggle.contains(event.target))) {
            sidebar.classList.remove('open');
        }
    });
    
    // Prévenir la fermeture quand on clique dans la sidebar
    if (sidebar) {
        sidebar.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }
});