// This script directly manipulates the DOM and loads the database's output
// into a table upon submitting the form.
document.addEventListener('DOMContentLoaded', function() {
    // An event listener is added to the submit button and the form fields
    // are iterated through and submitted.
    document.querySelector('form').addEventListener('submit', function() {
        input = {}
        for (let field of ['station', 'month', 'day', 'year'])
            input['${field}'] = document.querySelector('#${field}').value;
            
        // document.querySelector('#error_message').innerHTML = 'foo';

        // jQuery function makes a callback GET request to the /query route, and the whole 
        // site is not halted if the server takes a long time to respond. Table entries are
        // created in a loop and added inside of the empty table tag.
        $.get('/query?day=${day}&month=${month}&year=${year}&station=${station}', function(data) {
            let html = '';
            for (let value in data)
                html += '<tr> <th>${data[value].name}</th> <td>${data[value].value}</td> </tr>';
            document.querySelector('#output').innerHTML = html;
        });
    });
    // An event listener is added to the "Input History" button and a similar request is made
    // to the /history route that returns the session environmental variable to be input into
    // the empty table tag.
    document.querySelector('#input_history').addEventListener('click', function() {
        $.get('/history', function(history) {
            let html = '';
            for (let query in history)
                html += '<tr> <th>${query[value].name}</th> <td>${data[value].value}</td> </tr>';
            document.querySelector('#output').innerHTML = html;
        });

    });
});