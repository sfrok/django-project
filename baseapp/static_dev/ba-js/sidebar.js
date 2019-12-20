function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('active');
    document.querySelector('.overlay').style.display = 'block';
}

$(".sidebar-exit").click(function() {
    document.getElementById('sidebar').classList.toggle('active');
    document.querySelector('.overlay').style.display = 'none';
});

$(".overlay").click(function() {
    document.getElementById('sidebar').classList.toggle('active');
    document.querySelector('.overlay').style.display = 'none';
});
