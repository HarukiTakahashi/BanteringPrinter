import pygame
import subprocess
import compute_rhino3d.Util
import compute_rhino3d.Grasshopper as gh
import compute_rhino3d.Mesh as mesh
import rhino3dm
import threading
import json

class TetrisEdit():
    
    compute_rhino3d.Util.url = 'http://localhost:5000/'

    def __init__(self, s, num, grid_num_x=4, grid_num_y=3,grid_size = 50):
        self.screen = s
        self.num = num

        self.grid_num_x = grid_num_x
        self.grid_num_y = grid_num_y
        self.is_making = False

        self.grid_size = grid_size

        self.grid = [[0] * grid_num_y for _ in range(grid_num_x)]

    def draw(self, ox, oy):
        GRAY = (200,200,200)
        BLACK = (0,0,0)
        WHITE=(255,255,255)
        LIGHT_YELLOW = (255,255,100)
        RED = (255,0,0)
        LIGHT_BLUE = (150,150,255)
        
    # 配列に基づいてグリッドを描画
        for row in range(self.grid_num_y):
            for col in range(self.grid_num_x):
                x = ox + col * self.grid_size 
                y = oy + row * self.grid_size 
                if self.grid[col][row] == 1:
                    pygame.draw.rect(self.screen, LIGHT_BLUE, (x, y, self.grid_size, self.grid_size))
                else:
                    pygame.draw.rect(self.screen, GRAY, (x, y, self.grid_size, self.grid_size))
                pygame.draw.rect(self.screen, BLACK, (x, y, self.grid_size, self.grid_size), 1)  # グリッド線

    def validate(self):
        if self.is_all_zero():
            # print("全部0です")
            return False           
        if self.check_multiple_islands():
            #print("1の島が2つ以上あるよ")
            return False     
        if self.check_zero_islands():
            #print("0の島が1つ以上あるよ")
            return False     
        
        return True

    def toggle(self, pos):
        x = pos[0]
        y = pos[1]
        self.grid[x][y] = 1 - self.grid[x][y]

    
    # すべて0かどうかチェックする関数
    def is_all_zero(self):
        for row in self.grid:
            for element in row:
                if element != 0:
                    return False
        return True


    def dfs(self,visited, x, y):
        # 範囲外、または既に訪問済み、または値が0の場合は終了
        rows = self.grid_num_x
        cols = self.grid_num_y
        if x < 0 or x >= rows or y < 0 or y >= cols or visited[x][y] or self.grid[x][y] == 0:
            return
        # 現在のセルを訪問済みに設定
        visited[x][y] = True
        # 上下左右を探索
        self.dfs(visited, x + 1, y)
        self.dfs(visited, x - 1, y)
        self.dfs(visited, x, y + 1)
        self.dfs(visited, x, y - 1)

    # 島が1つだけかどうかチェックする関数
    def check_multiple_islands(self):
        rows = self.grid_num_x
        cols = self.grid_num_y
        visited = [[False for _ in range(cols)] for _ in range(rows)]
        island_count = 0  # 島の数をカウント

        for i in range(rows):
            for j in range(cols):
                if self.grid[i][j] == 1 and not visited[i][j]:
                    # 新しい島を発見
                    island_count += 1
                    if island_count > 1:
                        return True  # 島が2つ以上見つかったらTrueを返す
                    self.dfs(visited, i, j)

        return False  # 島が1つ以下の場合

    def recur_check(self, x, y, dx, dy):
        rows = self.grid_num_x
        cols = self.grid_num_y
        
        if self.grid[x][y] == 1:
            return 1
        if x+dx < 0 or x+dx >= rows or y+dy < 0 or y+dy >= cols:
            return 0
        
        if self.grid[x][y] == 0:
            return self.recur_check(x+dx, y+dy,dx, dy)
            
    
    # 0の島が作られていないかチェックする関数
    def check_zero_islands(self):
        rows = self.grid_num_x
        cols = self.grid_num_y

        for i in range(rows):
            for j in range(cols):
                if self.grid[i][j] == 0:
                    # 新しい島を発見
                    r = self.recur_check(i,j,1, 0)+self.recur_check(i,j,-1, 0)+self.recur_check(i,j,0, 1)+self.recur_check(i,j,0, -1)
                    if r == 4:
                        return True

        return False  # 島が1つ以下の場合
    
    
    # ============================================================
    def making(self):
        if not self.is_making:
            print("処理開始するよ")
            thread_a = threading.Thread(target=self.process)
            thread_a.start()
            self.is_making = True
    
    # モデルを生成してGcodeを作っておく
    def process(self):
        print("モデリングするよ")
        self.modeling()
        print("スライスするよ")
        self.slicing()
        self.is_making = False

    def save_mesh_as_stl(self, mesh, file_path="test.stl"):
        """
        rhino3dm.Mesh を STL ファイルに保存
        :param mesh: rhino3dm.Mesh オブジェクト
        :param file_path: 出力する STL ファイルのパス
        """
        print(file_path)
        with open(file_path, 'w') as stl_file:
            stl_file.write("solid mesh\n")
            
            # 面（Faces）をループ
            for i in range(len(mesh.Faces)):
                # 法線の計算（必要なら独自に計算可能）
                normal = (0.0, 0.0, 0.0)  # 法線がない場合のデフォルト値
                if i < len(mesh.Normals):
                    normal = (
                        mesh.Normals[i].X,
                        mesh.Normals[i].Y,
                        mesh.Normals[i].Z,
                    )
                stl_file.write(f"  facet normal {normal[0]} {normal[1]} {normal[2]}\n")
                stl_file.write("    outer loop\n")
                
                # 面に対応する頂点を取得
                face = mesh.Faces[i]
                vertex_indices = [face[0], face[1], face[2]]
                for index in vertex_indices:
                    vertex = mesh.Vertices[index]
                    stl_file.write(f"      vertex {vertex.X} {vertex.Y} {vertex.Z}\n")
                
                stl_file.write("    endloop\n")
                stl_file.write("  endfacet\n")
            
            stl_file.write("endsolid mesh\n")

    def modeling(self):
        input_trees = []
        tree = gh.DataTree("Position")
        count = 0
        for row in range(self.grid_num_x):
            for col in range(self.grid_num_y):
                if self.grid[row][col] == 1:
                    cs = {count}
                    tree.Append([cs], ["{\"X\":"+str(row*15)+",\"Y\":"+str(col*15)+",\"Z\":0.0}"])
                    input_trees.append(tree)
                    count+=1
        print(str(input_trees))
        output = gh.EvaluateDefinition('.curaengine\\mesh_hops.gh', input_trees)

        values = output['values']
        for value in values:
            name = value['ParamName']
            inner_tree = value['InnerTree']
            print(name)
            for path in inner_tree:
                print(path)
                values_at_path = inner_tree[path]
                for value_at_path in values_at_path:
                    data = value_at_path['data']
                    if isinstance(data, str) and 'archive3dm' in data:
                        obj = rhino3dm.CommonObject.Decode(json.loads(data))
                        print(obj)
                        print("hi!")
                        self.save_mesh_as_stl(obj,"M_S\\output_" +str(self.num)+".stl")
                    else:
                        print(data)
    
    
    
    def slicing(self):
        cmd = ".curaengine\\CuraEngine.exe slice -j .curaengine\\kingroon_kp3s_batering.def.json -o M_S\\output_" +str(self.num)+".gcode"
        cmd +=  " -l C:\\Users\\Haruki\\Documents\\GitHub\\BanteringPrinter\\M_S\\output_" +str(self.num)+".stl -s roofing_layer_count=1"
        subprocess.call(cmd.split())