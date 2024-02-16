import React from 'react';
import Redirect from './redirect';
import {BrowserRouter as Router} from 'react-router-dom';

function ViewCart() {
    
    const data = sessionStorage.getItem('data');
    const selection = data == null ? [] : JSON.parse(data);
      
    return <>
    
    <div className="App">
      
      <table>
        {
            selection.map(
                (data) => {
                    return (
                        <tr><td>{data.name}</td><td>{data.quantity}</td></tr>
                        )
                    }
                )
        }
      </table>
    </div>
    <Router>
      <Redirect id={""} name={"Back"}/>
    </Router>
    </>
}

export default ViewCart;