
// Function to reset search options
function remove_selected() {
    var custom_fields = {
        sexuality: "Sexuality ▾",
        height_max: "Max Height ▾",
        height_min: "Min Height ▾",
        distance: "Distance ▾"
    }
    
    $('.custom-form-field').each(function() {
        $(this).val('')
        let field_id = $(this).attr('id')
        $(this).siblings('.dropdown-toggle').find('.filter-option-inner-inner').text(custom_fields[field_id])
    });
    $('.search-form select').selectpicker('deselectAll');
    $('.dropdown-toggle').removeClass('selected-search-option');
}


// Ensure value of selected inputs remain on page load
var sexuality = $('#sexuality').data('sexuality')
if (sexuality) {
    var sexuality_arr = JSON.parse(sexuality.replace(/\'/g, "\""));
    $('#sexuality').val(sexuality_arr)
}
var min_height = $('#height_min').data('min-height');
var max_height = $('#height_max').data('max-height');
var distance = $('#distance').data('distance');
$('#height_max').val(max_height);
$('#height_min').val(min_height);
$('#distance').val(distance);

// Set titles of selected options to inputted values
var min_height_option = $('select[name="height_min"] option[value="' + min_height + '"]').text();
if(min_height_option) {
    $('.dropdown-toggle[data-id="height_min"] .filter-option-inner-inner').text(min_height_option);
}
var max_height_option = $('select[name="height_max"] option[value="' + max_height + '"]').text();
if(max_height_option) {
    $('.dropdown-toggle[data-id="height_max"] .filter-option-inner-inner').text(max_height_option);
}
var distance_option = $('select[name="distance"] option[value="' + distance + '"]').text();
if(distance_option) {
    distance_option
    $('.dropdown-toggle[data-id="distance"] .filter-option-inner-inner').text(distance_option);
}

// Set title of sexuality to inputted values
if(sexuality_arr){
    var sexuality_title = ""
    for(i=0; i < sexuality_arr.length; i++) {
        var sexuality_option = $('select[name="sexuality"] option[value="' + sexuality_arr[i] + '"]').text() 
        if(i == 0 || sexuality_arr.length == 0) {
            sexuality_title += sexuality_option
        } else {
            sexuality_title += ", "
            sexuality_title += sexuality_option
        }
    }
    $('.dropdown-toggle[data-id="sexuality"] .filter-option-inner-inner').text(sexuality_title);
}

// On select search options, change option's appearance
$('.search-form select').on('change', function() {
    if ($(this).val() == null) {
        $(this).siblings('.dropdown-toggle').removeClass('selected-search-option')
    }
    else {
        $(this).siblings('.dropdown-toggle').addClass('selected-search-option')
    }
});

// Initiliase selectpicker options
$('.search-form select').attr('data-container', 'body');
$('.search-form select').selectpicker();
$('.search-form select').attr('title', '');

// On load check if any options are selected and update styling
// Has to be after selectpicker
$('.search-form select').each(function() {
    if ($(this).val() != null && $(this).val() != "") {
        $(this).siblings('.dropdown-toggle').addClass('selected-search-option')
    }
});


