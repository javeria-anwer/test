import { useState, useEffect } from 'react';
import Redirect from './redirect';
import {BrowserRouter as Router} from 'react-router-dom';

function App() {  
  
  const [data, setData] = useState([]);
  const [value, setValue] = useState([])

  useEffect(() => {loaddata();},[])

  const loaddata = async () => {
    
    fetch("https://localhost:7140/api/Product/GetAllProducts")
    .then(response => {
      return response.json()
    })
    .then(data => {
      setData(data)
    })

  }

  function handleClick(id, name) {
    //the thing  you wanna do
    console.log();

    var txt_id = "textbox_"+ id;
    var val = document.getElementById(txt_id).value;
    console.log(val);

    const p: Product = {
      id: id,
      name: name,
      quantity: parseInt(val)
    };

    var data_set = value;
    var filtered = data_set.filter(function(el) { return el.id !== id; }); 
    filtered.push(p);

    sessionStorage.setItem('data', JSON.stringify(filtered));

    setValue(filtered);
  }


  return (
    <>
    
    <div className="App">
      
      <table>
        {
          data.map((data)=>{
              return (
                <tr>
                    <td>{data.Name}</td>
                    <td><input type='number' id={'textbox_'+data.Id} autoComplete="off"  min="0" max="100"></input></td>
                    <td><button onClick={() => handleClick(data.Id, data.Name)}>Add</button></td>
                </tr>)
              }
            )
          }
      </table>

    </div>

    <Router>
      <Redirect id={"viewCart"} name={"View Cart"}/>
    </Router>

    </>
  );
}

export default App;
