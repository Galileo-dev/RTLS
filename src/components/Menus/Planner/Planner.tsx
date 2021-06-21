import * as React from "react";
import styled from "styled-components";
import Dropdown from "react-dropdown";
import "react-dropdown/style.css";
import CustomDropDown from "../../Lib/CustomDropDown";

const options = [
  { name: "Jool" },
  { name: "Mun" },
  { name: "Minmus" },
  { name: "Kerbin" },
  { name: "Leo" },
];
const defaultOption = options[0];

function Planner() {
  const [ticker, setTicker] = React.useState("");
  const [destinations, setDestination] = React.useState("");
  const [selected_destination, setSelectedDestination] = React.useState("");
  React.useEffect(() => {
    window.addEventListener("pywebviewready", function () {
      if (!window.pywebview.state) {
        window.pywebview.state = {};
      }
      // Expose setTicker in order to call it from Python
      window.pywebview.state.setTicker = setTicker;

      window.pywebview.api
        .get_avail_destinations()
        .then((res) => setDestination(res));
    });
  }, []);

  return (
    <Container>
      <Content>
        <Box>
          <OutLinedBox width="75%">
            <BoxContainer>
              <Title>Mission Planner</Title>
              <Label>Status: {ticker}</Label>
              {/* <Label>From:</Label>
              <CustomDropDown
                options={options}
                width="75%"
                margin-bottom="50px"
              /> */}
              {/* <StyledDropdown options={options}  className="arrow-"  value={defaultOption} placeholder="Select an option" ></StyledDropdown> */}
              <Label>Desination:</Label>
              {destinations.length ? (
                <CustomDropDown options={destinations} width="75%" />
              ) : (
                <h1>Loading</h1>
              )}
              <Submit
                onClick={() => {
                  window.pywebview.api.set_window_size(700, 900);
                }}
              >
                Plan
              </Submit>
            </BoxContainer>
          </OutLinedBox>
        </Box>
      </Content>
    </Container>
  );
}

const Submit = styled.button`
  font-weight: bold;
  color: #f9f9f9;
  border-radius: 35px;
  background-color: #0063e5;
  margin: 12px;
  margin-top: 20px;
  width: 6em;
  border: 1px solid transparent;
  letter-spacing: 1.5px;
  font-size: 18px;

  padding: 12px;
  transition: all 0.2s ease 0s;

  -webkit-touch-callout: none; /* iOS Safari */
  -webkit-user-select: none; /* Safari */
  -khtml-user-select: none; /* Konqueror HTML */
  -moz-user-select: none; /* Old versions of Firefox */
  -ms-user-select: none; /* Internet Explorer/Edge */
  user-select: none; /* Non-prefixed version, currently
                                  supported by Chrome, Edge, Opera and Firefox */

  &:hover {
    background-color: #0483ee;
    cursor: pointer;
  }
  &:active {
    transform: scale(0.95);
  }
`;

const Title = styled.h1`
  text-align: center;
`;

const Label = styled.p`
  text-align: left;
  letter-spacing: 2px;
  color: ${(props) => props.theme.label};
  margin: 5px;
`;

const Container = styled.section`
  overflow: hidden;
  display: flex;
  flex-direction: column;
  text-align: center;
  height: calc(100vh - 70px);
`;

const Content = styled.section`
  margin-bottom: 10vw;
  width: 100%;
  position: relative;
  min-height: calc(100vh - 70px);
  box-sizing: border-box;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  padding: 80px 80px;
  height: 100%;
`;

const StyledDropdown = styled(Dropdown)`
  text-align: left;
  font-weight: bolder;
`;

const Box = styled.div`
  max-width: 650px;
  flex-wrap: wrap;
  display: flex;
  flex-direction: column;

  justify-content: center;
  margin-top: 0;
  align-items: center;
  text-align: left;
  transition-timing-function: ease-out;
  transition: opacity 0.2s;
  width: 100%;
`;

const OutLinedBox = styled.div`
  font-weight: normal;
  color: #f9f9f9;
  background-color: #1a1c48;
  width: ${(props) => props.width};
  border-radius: 15px;
  border: 2px solid ${(props) => props.theme.toggleBorder};
  letter-spacing: 1.5px;
  font-size: 18px;
  padding: 5px;
`;

const OutLinedInputBox = styled.input`
  width: 90%;
  padding: 20px;
  border-radius: 50px;
  border: 2px solid ${(props) => props.theme.toggleBorder};
  background-color: #131313;
  color: #f9f9f9;
  margin: 10px;

  &:focus {
    outline: none;
  }
`;

const BoxContainer = styled.div`
  padding: 5px 15px;
`;

export default Planner;
