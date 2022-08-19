//here you can build functions to call in the html files...just remember to connect your html file to this one
//for examples check the existing html files


// Showing nice alert of given message and type
function GrowlCall(msg,type){
    $(".bootstrap-growl").remove();
    $.bootstrapGrowl(msg, {
        ele: 'nav',
        type: type,
        offset: {from: 'top', amount: 20},
        align: 'center',
        width: 'auto',
        delay: 2000,
        allow_dismiss: false,
    });
}

// Checking if a patient exists
$('#search_btn').click(function () {
    console.log("search")
    let patient_id = $('#patient_input')[0].value
    let form = $('#search_form')
    $.get({
        url: "/patient_detail/check",
        data: {data: patient_id},
        success: function (result) {
            if (result === "False") {  //If patient already exist
                GrowlCall(" מטופל לא נמצא",'danger');
            } else {
                $('<input type="submit">').hide().appendTo(form).click().remove();
            }
        }
    })
})

//handles the button to schedule a new test
$("#make_new_test_btn").click(function () {
        console.log("new test b")
        let form = $('#new_test_form')
        let is_in_hospital = $('#is_in_hospital')[0].checked
        let email = $('#email')[0].value
        let date = $('#date')[0].value
        const token = $('input[name="csrfmiddlewaretoken"]').attr('value')
        $.post({
            url: "/patient_detail/make_new_test",
            data: {"is_in_hospital": is_in_hospital, "date": date, "email": email},
            headers: {
            "X-CSRFToken": token
            },
            success: function (result) {
                if (result === "False") {  //If something went wrong
                    GrowlCall("עדכון לא הצליח",'danger')
                    console.log("no")
                } else {
                    GrowlCall("עודכן בהצלחה!",'success')
                    console.log("yes")
                }
            }
        })
    })

//handles all edit buttons
function edit_btn(test_name,score,question,place){
    console.log("edit btn")
    let email = $('#email')[0].value
    const token = $('input[name="csrfmiddlewaretoken"]').attr('value')
        $.post({
            url: "edit_score",
            data: {"email": email, "score": score.value, "question": question, "place": place, "test": test_name.value},
            headers: {
            "X-CSRFToken": token
            },
            success: function (result) {
                if (result === "False") {  //If something went wrong
                    GrowlCall("עדכון לא הצליח",'danger')
                    console.log("no")
                } else {
                    console.log("yes")
                    GrowlCall("עדכון הצליח",'success')
                }
            }
        })
}



// returning formatted date
function formatDate(formated, date = null) {
    var dtToday;
    if (!date)
        dtToday = new Date()
    else
        dtToday = new Date(date)

    var month = dtToday.getMonth() + 1;
    var day = dtToday.getDate();
    var year = dtToday.getFullYear();
    if (month < 10)
        month = '0' + month.toString();
    if (day < 10)
        day = '0' + day.toString();

    if (formated)
        return [year, month, day].join('-'); // for init the date picker
    else
        return [day, month, year].join('-'); // for filter dates
}


//// Making the data for the chart
//function filterDatesAndLabels(isDefault, reports) {
//    let status_reports = []
//    let pointsStyles = []
//    let pointsColors = []
//    if (isDefault)
//        formated_today = formatDate(false)
//    else
//        formated_today = formatDate(false, date_picker.value)
//
//    for (const reportee of reports) {
//        new_label = reportee.label;
//        new_value = reportee.value;
//        new_label = new_label.split(' ')
//
//        if (new_label[0] === formated_today) {
//            if(reportee.hallucinations === 'True' && reportee.falls === 'True') {
//                pointsStyles.push('cross')
//                pointsColors.push('rgb(0,0,0)')
//            }
//            else if (reportee.hallucinations === 'True') {
//                pointsStyles.push('triangle')
//                pointsColors.push('rgb(255,82,82)')
//            }
//            else if(reportee.falls === 'True'){
//                pointsStyles.push('rect')
//                pointsColors.push('rgb(231, 161, 0)')
//            }else {
//                pointsStyles.push('circle')
//                pointsColors.push('rgb(39,65,181)')
//            }
//            report = {
//                x: new_label[1],
//                y: parseInt(new_value),
//            }
//            status_reports.push(report)
//        }
//    }
//    myChart.data.datasets[0].pointStyle = pointsStyles
//    myChart.data.datasets[0].pointBorderColor = pointsColors
//    myChart.data.datasets[0].data = status_reports;
//    myChart.data.datasets[0].pointBackgroundColor = pointsColors;
//    myChart.update();
//}

$("#id_email, #id_password1").on("blur", function () {
        $(this).css('box-shadow', "");
    })

$("#register_btn").click(function () {
    console.log("register btn")
    const email = $("#id_email")[0].value;
    const token = $('input[name="csrfmiddlewaretoken"]').attr('value');
    $.post({
        url: "/add_patient/validate_email",
        data: {
            email: email,
        },
        headers: {
            "X-CSRFToken": token
        },
        success: function (result) {
            if (result === "Valid") {  //If something went wrong
                GrowlCall("המשתמש הוסף בהצלחה", 'success')
                $('<input type="submit">').hide().appendTo($('form')).click().remove();
            } else if (result === "EmailExists") {
                GrowlCall("המשתמש כבר קיים", 'danger')
                $("#id_email").focus().css("box-shadow", "0 0 0 0.25rem rgb(255 0 0 / 25%)");
            } else if (result === "FillEmail") {
                $("#id_email").focus().css("box-shadow", "0 0 0 0.25rem rgb(255 0 0 / 25%)");
            }
        }
    })
})



