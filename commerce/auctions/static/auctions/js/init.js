 
document.addEventListener('DOMContentLoaded', function() {
    let elems = document.querySelectorAll('select');
    let instances = M.FormSelect.init(elems, {});
});

document.addEventListener('DOMContentLoaded', function() {
    const elems = document.querySelectorAll('.materialboxed');
    const instances = M.Materialbox.init(elems, {});
});