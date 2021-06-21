import React, { useState } from "react";
import styled from "styled-components";

//=========================== Drop Downs ====================================

const CenterContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
`

const DropDownContainer = styled.div`

  width:  ${(props) => props.width};
  margin: 0 auto;
  margin: 10px;
  font-weight: 700;
  color: white;
  display: inline-block;
  position: relative;
`;

const DropDownHeader = styled.div`
  border-radius: ${(props) => (props.isOpen ? "5px 5px 0px 0px" : "5px")};
  margin-bottom: ${(props) => (props.isOpen ? "2px" : "1px")};
  padding: ${(props) => (props.isOpen ? "5px" : "5px")};
  text-align: left;
  box-sizing: content-box;
  background: ${props => props.theme.foregroundLighter};
  border: 1.5px solid ${props => props.theme.toggleBorder};
  border-bottom: ${(props) => (props.isOpen ? "none" : "")};
  
`;

const DropDownListContainer =styled.div``;

const DropDownList = styled.ul`
  position: fixed;
  
  width:  100%;
  padding: 0;
  margin: 0;
  margin-top:-2px;
  background:${props => props.theme.foregroundLighter};
  border: 1.5px solid ${props => props.theme.toggleBorder};
  border-top: none;
  border-radius: 0px 0px 5px 5px;
  display: block;
  position: absolute;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;

`;

const ListItem = styled.li`
  list-style: none;
  text-align: left;
  padding: 5px;
  font-size: 100%;

  &:hover {
    background-color: #afafaf;

    cursor: pointer;
  }
`;

const CustomDropDown = (props) => {
  const [isOpen, setIsOpen] = useState(false);
  
  const toggling = () => setIsOpen(!isOpen);
  const [selectedOption, setSelectedOption] = useState(props.options[0]);
  const AvailbeToSelect = props.options.filter(CurrentOptions => CurrentOptions.name !== selectedOption.name);
  
  const onOptionClicked = (value, key) => () => {
    // var valueAndKey = []
    // valueAndKey.push(...value)
    // valueAndKey.push(key)
    setSelectedOption(value);
    setIsOpen(false);
  };

  return (
    <CenterContainer>
    <DropDownContainer width={props.width}>
      <DropDownHeader isOpen={isOpen} onClick={toggling}>
        {/* {selectedOption.image && <OptionImg src={selectedOption.image} />} */}
        {selectedOption.name}
      </DropDownHeader>
      {isOpen && (
        // <DropDownListContainer >
          <DropDownList width={props.width}>
            {AvailbeToSelect.map((option, key) => (
              <ListItem
                onClick={onOptionClicked(option, key)}
                key={Math.random()}
              >
                {option.image && <OptionImg src={option.image} />}
                {option.name}
              </ListItem>
            ))}
          </DropDownList>
        // </DropDownListContainer>
      )}
    </DropDownContainer>
    </CenterContainer>
  );
};

const OptionIcon = styled.img`
  height: 2em;
  vertical-align: middle;
  margin-right: 5px;
`;

const OptionImg = styled.img`
  vertical-align: middle;
  margin-right: 5px;
  width: 40px;
  height: 40px;
  object-fit: cover;
  border-radius: 50%;
  cursor: pointer;
`;

export default CustomDropDown;
