// let card_ids = JSON.parse('{{ card_ids }}');
    function showDropdown_cards(x){
        let y = card_ids;
        for(let i of y){
            let temp_id = "myDropdown-c"+i;
            let temp_element = document.getElementById(temp_id);
            if(temp_element.classList.length >= 1 && i!=x){
                temp_element.classList.remove("show");
            }
        }
        document.getElementById("myDropdown-c"+x).classList.toggle("show");
    }
    window.onclick = function (event) {
        if (!event.target.matches('.dropbtn')) {
            for(let i of card_ids){
            let temp_id = "myDropdown-c"+i;
            let temp_element = document.getElementById(temp_id);
            if(temp_element.classList.length >= 1){
                temp_element.classList.remove("show");
            }
        }
        }
    }
    function validateDate(id) {
        var UserDate = document.getElementById('card_deadline-'+id).value;
        var ToDate = new Date();
        console.log(UserDate)

        if (new Date(UserDate).getTime() < ToDate.getTime()) {
            alert("The deadline cannot not be before today's date");
            return false;
        }
        return true;
    }