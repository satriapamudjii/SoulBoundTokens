// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/// @title SoulboundToken (SBT)
/// @notice Implements an ERC721 Soulbound Token that cannot be transferred, making it permanently owned by the initial recipient.
contract SoulboundToken is ERC721, Ownable {
    /// @notice Emitted when a new token is issued.
    /// @param to The recipient of the token.
    /// @param tokenId The ID of the token issued.
    event Issue(address indexed to, uint256 indexed tokenId);

    /// @dev Current ID of the latest token minted, used to generate new token IDs.
    uint256 private _currentTokenID = 0;

    /// @notice Initializes the contract by setting a `name` and a `symbol` to the token collection.
    constructor() ERC721("SoulboundToken", "SBT") {}

    /// @notice Allows the owner to issue a new token to a specified address.
    /// @param to The recipient of the newly minted token.
    function issue(address to) public onlyOwner {
        uint256 newTokenId = _getNextTokenID();
        _incrementTokenID();
        _safeMintToken(to, newTokenId);
    }

    /// @notice Returns if the specified owner owns the given token.
    /// @param owner The address of the owner to check.
    /// @param tokenId The token ID to check for ownership.
    /// @return `true` if the owner owns the token, otherwise `false`.
    function isOwnerOf(address owner, uint256 tokenId) public view returns (bool) {
        return ownerOf(tokenId) == owner;
    }

    /// @dev Safely mints a token and emits the Issue event.
    /// @param to The address that will own the minted token.
    /// @param tokenId The token ID to mint.
    function _safeMintToken(address to, uint256 tokenId) internal {
        _safeMint(to, tokenId);
        emit Issue(to, tokenId);
    }

    /// @dev Gets the next token ID for minting by returning the current token ID.
    /// @return The next token ID.
    function _getNextTokenID() internal view returns (uint256) {
        return _currentTokenID;
    }

    /// @dev Increments the counter for the current token ID to ensure unique token IDs for new mints.
    function _incrementTokenID() internal {
        _currentTokenID += 1;
    }

    /// @dev Ensures tokens are non-transferable by throwing if a transfer is attempted.
    /// @param from Sending address.
    /// @param to Receiving address.
    /// @param tokenId ID of the token being transferred.
    function _beforeTokenTransfer(address from, address to, uint256 tokenId) internal override {
        require(from == address(0), "SoulboundToken: Tokens cannot be transferred.");
        super._beforeTokenTransfer(from, to, tokenId);
    }

    /// @dev Disables token approval functionality.
    function approve(address to, uint256 tokenId) public override {
        revert("SoulboundToken: Token approval is disabled.");
    }

    /// @dev Disables setting approval for all functionality.
    function setApprovalForAll(address operator, bool approved) public override {
        revert("SoulboundToken: Token approval is disabled.");
    }
}