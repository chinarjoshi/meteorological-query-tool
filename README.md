## Meteorological Query Tool
    -created by Chinar Joshi

The purpose of the MQT is to provide a statistical representation of climate data
from 30 years ago to today from numerous meteorological stations across the United States. This is 
done though the use of the National Climate Data Center's database and a web application to provide 
a seamless user interface. All queries are conducted in log(n) time complexity due to the use of SQL
indexes. The user can query data from a specific date or create a visualization of climate trends
using the Matplotlib library.

## Technologies
**Server Side**
Python + Flask render the site and return jsons containing database output.
SQLite is the relational database management system used to allow for queries
    in log(n) time complexity using B-Trees.

**Client Side**
__HTML__ structures each website route and provides a formatted form.
__CSS + Bootstrap__ format the websites and makes them visually appealing.
__Javascript + jQuery__ handle client-side control flow and make callback GET
    requests through AJAX to avoid server-dependent performance.

This application was developed in Emacs.

## How to use
If the web application cannot be accessed, run
    pip install "requirements.txt"
    flask run
to start a development server.
Note: you may have to initally refresh page.

## TODO
    -Manipulate the DOM using jQuery and AJAX calls. When the submit button is pressed,
    make a GET request to the server using the input fields.
    PROBLEM: When the HTML form is submitted, the corresponding JS event listener does
    not reccognize the event, likely due to syntax error because of confusion between
    element vs id JS syntax. Figure out how to properly select DOM elements.

    -Allow a range of dates to be selected on the HTML file and render coordinate plot
    using the database response. Use this instead of table.

    -Change the padding and color of the Bootstrap classes in styles.css to center the
    input fields and make the background sky blue.
