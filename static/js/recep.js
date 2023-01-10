function appoint(){

    var x = document.getElementById("appoint");
    x.style.display = "block";

    var y = document.getElementById("bill"); 
    y.style.display = "none";
}

function bill(){

    var x = document.getElementById("appoint");
    x.style.display = "none";
    
    var y = document.getElementById("bill"); 
    y.style.display = "block";
}


function result(){
    var x = document.getElementByClass("result");
    
    x.style.display="block";
    
}
