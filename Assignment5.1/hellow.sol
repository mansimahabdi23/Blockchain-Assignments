//SPDX-License-Identifier: MIT
pragma solidity ^0.7.4;

contract hello {
    string enter;

    function set(string memory value) public {
        enter = value;
    }

    function get() public view returns (string memory) {
        return enter;
    }
}