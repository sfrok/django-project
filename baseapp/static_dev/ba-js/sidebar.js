function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('active');
    document.querySelector('.overlay-base').style.display = 'block';
}

$(".sidebar-exit").click(function() {
    document.getElementById('sidebar').classList.toggle('active');
    document.querySelector('.overlay-base').style.display = 'none';
});

$(".overlay-base").click(function() {
    document.getElementById('sidebar').classList.toggle('active');
    document.querySelector('.overlay-base').style.display = 'none';
});
