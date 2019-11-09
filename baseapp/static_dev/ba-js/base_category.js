function heightSidebar() {
    let a = $(".height_content").height();
    let b = $(".sidebar").height();
    if (a > b) {
        $(".sidebar").height(a);
    }
}