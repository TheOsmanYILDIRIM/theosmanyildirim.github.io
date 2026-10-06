# Voxel Architect Studio handoff

- Pages path: `/voxel-architect/`.
- Delivery stays a single self-contained `index.html`; development may be split locally but published output is one HTML.
- Goal: AI-generated parametric VoxelBuild plans compile to voxel geometry, preview in-browser, then export to Luanti/WorldEdit.
- Current primitives: wall, box, round_tower, gate, battlement, clear.
- Current sample: a multi-wall castle with four round towers, gate, keep and battlements; it auto-builds on page load.
- Embedded block textures currently come from the Luanti/Minetest Game repository and use real node names.
- Next priority: polygon walls, arches, roofs, roads, bridges, connectors/anchors, terrain adaptation and a VoxelManip-oriented Luanti builder export.
- Keep this file concise: replace stale status instead of appending an endless log.
