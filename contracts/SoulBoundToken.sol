// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/// @title SoulboundToken (SBT)
/// @notice Implements an ERC721 Soulbound Token that cannot be transferred, making it permanently owned by the initial recipient.
contract SoulboundToken is ERC721, Ownable {
    /// @notice Emitted when a new token is issued.
    /// @param recipient The recipient of the token.
    /// @param tokenId The ID of the token issued.
    event TokenIssued(address indexed recipient, uint256 indexed tokenId);

    /// @dev Current ID of the latest token minted, used to generate new token IDs.
    uint256 private nextTokenId = 0;

    /// @notice Initializes the contract by setting a `name` and a `symbol` for the token collection.
    constructor() ERC721("SoulboundToken", "SBT") {}

    /// @notice Allows the owner to issue a new token to a specified recipient.
    /// @param recipient The recipient of the newly minted token.
    function issueToken(address recipient) public onlyOwner {
        uint256 tokenId = _getNextId();
        _incrementId();
        _mintTokenSafely(recipient, tokenId);
    }

    /// @notice Verifies if the specified owner owns the given token.
    /// @param owner Address of the potential owner to verify.
    /// @param tokenId ID of the token to verify ownership.
    /// @return `true` if the owner indeed owns the token, otherwise `false`.
    function ownsToken(address owner, uint256 tokenId) public view returns (bool) {
        return ownerOf(tokenId) == owner;
    }

    /// @dev Mints a token safely and emits the TokenIssued event.
    /// @param recipient Address that will be assigned ownership of the minted token.
    /// @param tokenId ID of the token to mint.
    function _mintTokenSafely(address recipient, uint256 tokenId) internal {
        _safeMint(recipient, tokenId);
        emit TokenIssued(recipient, tokenId);
    }

    /// @dev Generates the next token ID for minting by returning the current counter.
    /// @return The next unique token ID.
    function _getNextId() internal view returns (uint256) {
        return nextTokenId;
    }

    /// @dev Increases the token ID counter to ensure uniqueness for future mints.
    function _incrementId() internal {
        nextTokenId += 1;
    }

    /// @dev Overrides the transfer functionality to prevent token transfers, only allowing minting.
    /// @param from Address attempting to send the token (should always be the zero address for minting).
    /// @param to Address receiving the token.
    /// @param tokenId ID of the token being minted.
    function _beforeTokenTransfer(address from, address to, uint256 tokenId) internal override {
        require(from == address(0), "SoulboundToken: Tokens are non-transferable.");
        super._beforeTokenTransfer(from, to, tokenId);
    }

    /// @dev Disables the approval of token transfers.
    function approve(address to, uint256 tokenId) public override {
        revert("SoulboundToken: Approval of token transfers is disabled.");
    }

    /// @dev Disables the approval for all tokens.
    function setApprovalForAll(address operator, bool approved) public override {
        revert("SoulboundToken: Approval for all tokens is disabled.");
    }
}