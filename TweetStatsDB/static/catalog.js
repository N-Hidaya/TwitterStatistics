function send2Server(when, who, comment, about, media, what, whom, refID) {
    $.ajax({
        url:"/catalog",
        method: "POST",
        data: {when:when,who:who,comment:comment,about:about, media:media, what:what, whom:whom, referenceID:refID},
        error: function(){
            alert("Error");
        },
        success: function(data,status,xhr){

            catalogData = [];
            for (var info of data.catalogData){
                catalogData.push(info);
            }
            submit(catalogData);
        }
    })
}

function submit(catalogData) {

    //hide input form
    document.getElementById("form").style.display = "none";
    

    //output values
    document.querySelector(".output_when").innerHTML = catalogData.when;
    document.querySelector(".output_who").innerHTML = catalogData.who;
    document.querySelector(".output_comment").innerHTML = catalogData.comment;
    document.querySelector(".output_about").innerHTML = catalogData.about;
    document.querySelector(".output_media").innerHTML = catalogData.media;
    document.querySelector(".output_what").innerHTML = catalogData.what;
    document.querySelector(".output_whom").innerHTML = catalogData.whom;
    document.querySelector(".output_refID").innerHTML = catalogData.refID;

    //show output 
    document.getElementById("output_table").style.display = "block";
    


}

//call submit handling function
document.querySelector("#submit").addEventListener("click", submit);