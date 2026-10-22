# Team collaboration

One repository contains all three alternatives so shared styling, evidence and presentation content stay together.

## Access

Aarya is the repository owner. Intended collaborators receive **Write** access after accepting their GitHub invitation.

| Teammate | GitHub username | Resolution |
| --- | --- | --- |
| Aarya Deshpande | AaryaDeshpande | Connected GitHub account and team screenshot |
| Tanya Sharma | Tanya-duke | Supplied directly in team screenshot |
| Ishan Madan | ishan-madan | Supplied directly in team screenshot |
| Jason Dorman | Not yet supplied | Ask Jason for his exact username before inviting |

This table records the intended setup. It does not assert that a repository or invitations already exist.

## Start working

After accepting the invitation, use the repository's green **Code** button to copy its actual clone URL. Clone it, then:

```sh
cd referralflow-ai
git switch -c your-name/short-change-description
npm start
```

Edit the relevant file, check it in a browser at desktop and phone widths, and run `npm test`. To share the change:

```sh
git add .
git commit -m "Describe the user-facing change"
git push -u origin HEAD
```

Open a pull request on GitHub. Write access permits direct pushes, but branches and short reviews make simultaneous edits easier to coordinate.

## Keep work grounded

- Keep specialist review and approval before any approved export.
- Preserve unknown source information and fictional-data labels.
- Retain the distinction between demonstrated local behavior and simulated AI/roles/delivery.
- Preserve an already delivered snapshot when editing a later draft, as the current design implements.
- Check shared `dist/site.css` and `dist/nav.css` changes in A, B, C and the hub. The left rail markup is repeated in each page (and in `build-log.py` for the prompt log), so update every copy when adding a rail link.
- Record new development prompts honestly. Do not fabricate customer findings or team rehearsals.
- Agree on changes to the product direction before restructuring the concept.

The proposed remote repository is private. Public demo links can remain separate from code access.
