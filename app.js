const form=document.getElementById("translatorForm");

const loading=document.getElementById("loading");

const urdu=document.getElementById("urdu");

const count=document.getElementById("count");

const textarea=document.getElementById("english");

textarea.addEventListener("input",()=>{

count.innerHTML=textarea.value.length;

});

form.addEventListener("submit",async(e)=>{

e.preventDefault();

loading.style.display="block";

urdu.innerHTML="";

const response=await fetch("/translate",{

method:"POST",

headers:{

"Content-Type":"application/json"

},

body:JSON.stringify({

text:textarea.value

})

});

const data=await response.json();

loading.style.display="none";

urdu.innerHTML=data.translation;

});

document.getElementById("copyBtn").onclick=()=>{

navigator.clipboard.writeText(urdu.innerText);

alert("Copied!");

}