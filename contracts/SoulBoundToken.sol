// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract SoulboundToken is ERC721, Ownable {
    event Issue(address indexed to, uint256 indexed tokenId);

    constructor() ERC721("SoulboundToken", "SBT") {}

    uint256 private _currentTokenID = 0;

    function issue(address to) public onlyOwner {
        uint256 newTokenId = _getNextTokenID();
        _incrementTokenID();
        _safeMintToken(to, newTokenId);
    }

    function _safeMintToken(address to, uint256 tokenId) internal {
        _safeMint(to, tokenId);
        emit Issue(to, tokenId);
    }

    function _getNextTokenID() internal view returns (uint256) {
        return _currentTokenID;
    }

    function _incrementTokenID() internal {
        _currentTokenID++;
    }

    function _beforeTokenTransfer(address from, address to, uint256 tokenId) internal override {
        require(from == address(0), "SoulboundToken: Tokens cannot be transferred.");
        super._beforeTokenTransfer(from, to, tokenId);
    }

    function approve(address to, uint256 tokenId) public override {
        revert("SoulboundToken: Token approval is disabled.");
    }

    function setApprovalForAll(address operator, bool approved) public override {
        revert("SoulboundToken: Token approval is disabled.");
    }

    function isOwnerOf(address owner, uint256 tokenId) public view returns (bool) {
        return ownerOf(tokenId) == owner;
    }
}