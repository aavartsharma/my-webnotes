let button1 = document.getElementById('ep-47button');
//button1.addEventListener('onclick',hide('para47'));
console.log(button1);
function hide(id) {
    let para=document.getElementById(id);
    if (para.style.display != 'none')
    {
        para.style.display='none';
    }
    else
    {
        para.style.display='block';
    }
}
    
