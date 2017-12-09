import React from 'react';


function unfold (elements) {
    return <ul>{elements.map(el => {
        if (el.hasOwnProperty('likes')) {
            return <li>
                <p><b>{el.key}</b>{el.likes}</p>
            </li>
        } else {
            return unfold(el.values)
        }
    })}</ul>
}
export default function (props) {
    console.log("These props:", props)
    return unfold(props)
}