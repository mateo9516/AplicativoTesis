function Dislike (boton,dato){
    $(boton).slideToggle();
    $(document.getElementById("L"+dato)).slideToggle();
    $(document.getElementById("mm"+dato)).slideToggle();
    $.getJSON( "https://apitesisjson.herokuapp.com/votos", function( json ) {
        //Dato es el nombre de la resu
        //json tiene el papel de BD        
        let temporal =[];
        var direccion
        for( let resu in json){
            var cambio = 0;
            if( json[resu]["resolucion"] == dato){
                json[resu]["Dislikes"] = parseInt(json[resu]["Dislikes"])+1; 
                cambio = 1;
                console.log(json[resu]);
                direccion = "https://apitesisjson.herokuapp.com/votos/" + json[resu]['id'];
                $.ajax({
                    url: direccion,
                    method:"PUT",
                    success: (res) => console.log("Se actualizo con exito"),
                    error: () => console.log("Hay un error"),
                    data: json[resu]
                });
                temporal.push(json[resu])
                //Aqui va el promedio
                document.getElementById("tt"+dato).innerText = String(((parseInt(json[resu]["Likes"])*100)/(parseInt(json[resu]["Dislikes"])+parseInt(json[resu]["Likes"]))))+"%"+"\nAprobación"
                $(document.getElementById("tt"+dato)).slideToggle();
            }
            if(cambio == 0){
                temporal.push(json[resu])
            }
        }
        //$.post( "/static/DB/retos.json", temporal );
    });
}

function Like (boton,dato){
    $(boton).slideToggle();
    $(document.getElementById("g"+dato)).slideToggle();
    $(document.getElementById("mm"+dato)).slideToggle();
    $.getJSON( "https://apitesisjson.herokuapp.com/votos", function( json ) {
        //Dato es el nombre de la resu
        //json tiene el papel de BD
        let temporal =[];
        var direccion
        for( let resu in json){
            var cambio = 0;
            if( json[resu]["resolucion"] == dato){
                json[resu]["Likes"] = parseInt(json[resu]["Likes"])+1; 
                cambio = 1;
                console.log(json[resu]);
                direccion = "https://apitesisjson.herokuapp.com/votos/" + json[resu]['id'];
                $.ajax({
                    url: direccion,
                    method:"PUT",
                    success: (res) => console.log("Se actualizo con exito"),
                    error: () => console.log("Hay un error"),
                    data: json[resu]
                });
                temporal.push(json[resu])
                //Aqui va el promedio
                document.getElementById("tt"+dato).innerText = String(((parseInt(json[resu]["Likes"])*100)/(parseInt(json[resu]["Dislikes"])+parseInt(json[resu]["Likes"]))))+"%"+"\nAprobación"
                $(document.getElementById("tt"+dato)).slideToggle();
            }
            if(cambio == 0){
                temporal.push(json[resu])
            }
        }
        //$.post( "/static/DB/retos.json", temporal );
    });
}

function spinner(){
    $(document.getElementById("PantallaCarga")).slideToggle();
}