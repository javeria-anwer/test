import React from 'react';
import {
  useNavigate,
  useParams,
} from 'react-router-dom';

export default function Redirect(props) {
  const navigate = useNavigate();
  let id  = props.id;
  let name  = props.name;

  const handleClick = () => {
    // 👇️ navigate programmatically
    // navigate('/'+id);
    window.location.replace("http://localhost:3000/"+id);
  };

  return (
    <div>
      <button onClick={handleClick}>{name}</button>
    </div>
  );
}