import styled from "styled-components";

// Props: background color, hover color
const CustomButton = styled.button`
  background-color: ${(props) => props.bg || "#FF964F"};   // default orange
  color: ${(props) => props.color || "white"};
  width: 250px;
  padding: 20px 0;
  font-size: 24px;
  border-radius: 10px;
  text-transform: uppercase;
  cursor: pointer;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
  transition: all 250ms ease;
  border: none;

  &:hover {
    background-color: ${(props) => props.hover || "black"};  // default hover black
    transform: scale(1.05);
  }
`;

export default CustomButton;