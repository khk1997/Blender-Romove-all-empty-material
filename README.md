# Blender-Romove-all-empty-material

Blender Python script for cleaning material slots and unused data.

執行時會處理目前選取的 Mesh 物件，並在清理後還原原本的選取狀態。

## 功能說明

1. 移除未被面使用的材質槽
2. 移除空的材質槽
3. 清掉 Blender 裡沒有使用者的 orphan data

如果物件的面目前只指到空白材質槽，script 會保留第一個非空材質並讓面改用它，避免清理後物件沒有任何材質。
