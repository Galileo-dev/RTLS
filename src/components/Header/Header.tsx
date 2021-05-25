import * as React from 'react'
import styled from 'styled-components'


export default function Header() {
  return (
    <div></div>
  //   <Nav>
  //       <NavMenu>
  //         {/* Home */}
  //         <a>
  //           <span>HOME</span>
  //         </a>
  //         {/* // */}
  //         <a>
  //           <span>SEARCH</span>
  //         </a>
  //         {/* // */}
  //         <a>
  //           <span>WATCHLIST</span>
  //         </a>
  //         {/* // */}
  //         <a>
  //           <span>WATCHING</span>
  //         </a>

  //         <a>
  //           <span>MOVIES</span>
  //         </a>

  //         <a>
  //           <span>SERIES</span>
  //         </a>
  //       </NavMenu>
  // </Nav>
  );
};

const Nav = styled.div`
  height: 70px;
  background: #1A1C48;
  display: flex;
  align-items: center;
  padding: 0 36px;
  position: fixed;
  bottom: 0;
  width: 100%;
  

  -webkit-touch-callout: none; /* iOS Safari */
  -webkit-user-select: none; /* Safari */
  -khtml-user-select: none; /* Konqueror HTML */
  -moz-user-select: none; /* Old versions of Firefox */
  -ms-user-select: none; /* Internet Explorer/Edge */
  user-select: none; /* Non-prefixed version, currently
                                  supported by Chrome, Edge, Opera and Firefox */
`;

const NavMenu = styled.div`
  display: flex;
  flex: 1;

  justify-content: center;
  align-items: center;
  a {
    display: flex;
    align-items: center;
    margin: 0 16px;
    cursor: pointer;

    span {
      font-size: 13px;
      letter-spacing: 1.42;
      position: relative;

      &:after {
        content: "";
        height: 2px;
        background: #f9f9f9;
        position: absolute;
        left: 0;
        right: 0;
        bottom: -6px;
        opacity: 0;
        transform-origin: left center;
        border-radius: 1px;
        transform: scaleX(0);
      }
    }
    &:hover {
      span:after {
        opacity: 1;
        transform: scaleX(1);
        transition-timing-function: ease-in;
        transition: 0.5s;
      }
    }
  }
`;
