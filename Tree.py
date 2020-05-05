# coding:utf-8
from json import dumps


class Node():
    def __init__(self, value=None):
        self.value = value
        self.rchild = None
        self.lchild = None
        self.balancefactor = 0


class Tree():
    def __init__(self):
        self.root = None
        self.anotherroot = None
        self.taller = False
        self.shorter = False

    def search(self, value) -> Node:
        # 寻找二叉平衡树中值为value的节点,如果找到则返回value所在节点,否则返回空节点

        # 从根开始遍历
        root = self.root
        # 不为空
        while root:
            # 如果value较小往左子树寻找
            if value < root.value:
                root = root.lchild
            # 如果相等跳出循环
            elif value == root.value:
                break
            # 如果value较大往右子树寻找
            else:
                root = root.rchild

        # 如果找得到则返回节点否则返回None
        return root

    def insert(self, data: int, choice='root'):
        # 如果Node节点不在二叉树中则插入Node

        def LeftRotate(node: Node) -> Node:
            '''
            :return 返回修改后的节点
            :param  node 将要左旋的节点
            '''

            # 右节点
            rc = node.rchild
            # node的右节点连接rc的左节点
            node.rchild = rc.lchild
            # rc的左节点连接node
            rc.lchild = node
            # 修改node的指向
            node = rc

            # 返回修改过的node
            return node

        def RightRotate(node: Node) -> Node:
            '''
            :return 返回修改后的节点
            :param  node 将要左旋的节点
            '''

            # 左节点
            lc = node.lchild
            # node的左节点连接lc的右节点
            node.lchild = lc.rchild
            # lc的右节点连接node
            lc.rchild = node
            # 修改node的指向
            node = lc

            # 返回修改过的node
            return node

        def LeftBalance(node: Node) -> Node:
            lc = node.lchild

            # 如果左子树的平衡因子为1只需要右旋
            if lc.balancefactor == 1:
                lc.balancefactor = node.balancefactor = 0
                node = RightRotate(node)

            # 如果左子树的平衡因子为-1需要先左旋后右旋
            elif lc.balancefactor == -1:
                # 左子树的右子树
                rc = lc.rchild

                # 如果右子树的平衡因子为0,则先左旋后右旋之后node和lc的平衡因子均为0
                if rc.balancefactor == 0:
                    node.balancefactor = lc.balancefactor = 0

                # 如果右子树的平衡因子为1,则先左旋后右旋之后node和lc的平衡因子如下
                elif rc.balancefactor == 1:
                    node.balancefactor = -1
                    lc.balancefactor = 0
                # 如果右子树的平衡因子为-1，则先左旋后右旋之后node和lc的平衡因子如下
                else:
                    node.balancefactor = 0
                    lc.balancefactor = 1
                rc.balancefactor = 0
                node.lchild = LeftRotate(node.lchild)
                node = RightRotate(node)
            # 返回节点值
            return node

        def RightBalance(node: Node) -> Node:
            # 右孩子
            rc = node.rchild

            # 如果右孩子的平衡因子为-1直接左旋
            if rc.balancefactor == -1:
                rc.balancefactor = node.balancefactor = 0
                node = LeftRotate(node)

            # 如果右孩子的平衡因子为1需要先右旋再左旋
            elif rc.balancefactor == 1:
                # 右孩子的左孩子
                lc = rc.lchild

                # 如果lc平衡因子为0，node、rc平衡因子都为0
                if lc.balancefactor == 0:
                    node.balancefactor = rc.balancefactor = 0
                # 如果lc平衡因子为1，node、rc平衡因子如下
                elif lc.balancefactor == 1:
                    node.balancefactor = 0
                    rc.balancefactor = -1
                # 如果lc平衡因子为1，node、rc平衡因子如下
                elif lc.balancefactor == -1:
                    rc.balancefactor = 0
                    node.balancefactor = 1
                # 设置lc的平衡因子为0
                lc.balancefactor = 0
                # 右旋
                node.rchild = RightRotate(node.rchild)
                # 左旋
                node = LeftRotate(node)
            return node

        def insertvalue(node: Node):
            # 如果node为空，则将data插到树中并把taller置为True
            if node == None:
                node = Node(data)
                self.taller = True
                # if None == self.root:
                #     self.root = node
            # 如果node不为空，则继续判断
            else:
                # 如果data等于node的值直接返回false
                if data == node.value:
                    print("Now the balanced tree already has the ", data)
                    return False, node

                # 如果data小于node的值则递归左子树并判断插入的位置
                elif data < node.value:
                    # 如果往左子树中已经存在该节点，置taller为false并返回
                    result, node.lchild = insertvalue(node.lchild)
                    if result == False:
                        self.taller = False
                        return False, node

                    # 如果平衡树长高了需要单独处理
                    if self.taller == True:

                        # 如果平衡因子为0即之前左右等高则置balancefactor为1并将taller置为True
                        if node.balancefactor == 0:
                            node.balancefactor = 1
                            self.taller = True
                        # 如果平衡因子为1即之前左比右高则经过左平衡之后子树的深度不变,将taller置为false
                        elif node.balancefactor == 1:
                            node.balancefactor = 1
                            node = LeftBalance(node)
                            self.taller = False
                        # 如果平衡因子为-1即之前右比左高则置balancefactor为0,子树的深度不变,将taller置为false
                        else:
                            node.balancefactor = 0
                            self.taller = False

                # 如果data大于node的值则递归右子树并判断插入的位置
                else:
                    result, node.rchild = insertvalue(node.rchild)
                    # 如果往右子树中已经存在该节点，置taller为false并返回
                    if result == False:
                        self.taller = False
                        return False, node

                    if self.taller == True:
                        # 如果平衡因子为0即之前左右等高，则置balancefactor为-1，右子树增加，将taller置为True
                        if node.balancefactor == 0:
                            node.balancefactor = -1
                            self.taller = True
                        # 如果平衡因子为-1即之前右比左高，则右平衡之后深度不变，将taller置为False
                        elif node.balancefactor == -1:
                            node.balancefactor = -1
                            node = RightBalance(node)
                            self.taller = False
                        # 如果平衡因子为1即左比右高，则置为0，深度不变将taller置为false
                        else:
                            node.balancefactor = 0
                            self.taller = False

            return True, node

        if choice == 'root':
            self.root = insertvalue(self.root)[1]
        elif choice == 'anotherroot':
            self.anotherroot = insertvalue(self.anotherroot)[1]

    def show(self, node):
        # 递归凹凸展示树

        def display(node, incident=0):
            if node != None:
                print(' '*incident, node.value)
                display(node.lchild, incident+2)
                display(node.rchild, incident+2)
        display(node)

    def delete(self, value, string):

        # 删除值为value的节点

        def LeftRotate(node: Node) -> Node:
            '''
            :return 返回修改后的节点
            :param  node 将要左旋的节点
            '''

            # 右节点
            rc = node.rchild
            # node的右节点连接rc的左节点
            node.rchild = rc.lchild
            # rc的左节点连接node
            rc.lchild = node
            # 修改node的指向
            node = rc

            # 返回修改过的node
            return node

        def RightRotate(node: Node) -> Node:
            '''
            :return 返回修改后的节点
            :param  node 将要左旋的节点
            '''

            # 左节点
            lc = node.lchild
            # node的左节点连接lc的右节点
            node.lchild = lc.rchild
            # lc的右节点连接node
            lc.rchild = node
            # 修改node的指向
            node = lc

            # 返回修改过的node
            return node

        def LeftBalance(node: Node) -> Node:
            lc = node.lchild

            # 如果左子树的平衡因子为1只需要右旋
            if lc.balancefactor == 1:
                lc.balancefactor = node.balancefactor = 0
                node = RightRotate(node)

            # 如果左子树的平衡因子为-1需要先左旋后右旋
            elif lc.balancefactor == -1:
                # 左子树的右子树
                rc = lc.rchild

                # 如果右子树的平衡因子为0,则先左旋后右旋之后node和lc的平衡因子均为0
                if rc.balancefactor == 0:
                    node.balancefactor = lc.balancefactor = 0

                # 如果右子树的平衡因子为1,则先左旋后右旋之后node和lc的平衡因子如下
                elif rc.balancefactor == 1:
                    node.balancefactor = -1
                    lc.balancefactor = 0
                # 如果右子树的平衡因子为-1，则先左旋后右旋之后node和lc的平衡因子如下
                else:
                    node.balancefactor = 0
                    lc.balancefactor = 1
                rc.balancefactor = 0
                node.lchild = LeftRotate(node.lchild)
                node = RightRotate(node)
            # 返回节点值
            return node

        def RightBalance(node: Node) -> Node:
            # 右孩子
            rc = node.rchild

            # 如果右孩子的平衡因子为-1直接左旋
            if rc.balancefactor == -1:
                rc.balancefactor = node.balancefactor = 0
                node = LeftRotate(node)

            # 如果右孩子的平衡因子为1需要先右旋再左旋
            elif rc.balancefactor == 1:
                # 右孩子的左孩子
                lc = rc.lchild

                # 如果lc平衡因子为0，node、rc平衡因子都为0
                if lc.balancefactor == 0:
                    node.balancefactor = rc.balancefactor = 0
                # 如果lc平衡因子为1，node、rc平衡因子如下
                elif lc.balancefactor == 1:
                    node.balancefactor = 0
                    rc.balancefactor = -1
                # 如果lc平衡因子为1，node、rc平衡因子如下
                elif lc.balancefactor == -1:
                    rc.balancefactor = 0
                    node.balancefactor = 1
                # 设置lc的平衡因子为0
                lc.balancefactor = 0
                # 右旋
                node.rchild = RightRotate(node.rchild)
                # 左旋
                node = LeftRotate(node)
            return node

        def DelNode(pre: Node, node: Node, value):
            # 删除节点node

            # 如果node为空返回False和node
            if node == None:
                return False, node

            # 如果当前节点值等于value则删除
            if node.value == value:

                if node.rchild == None and node.lchild == None:
                    self.shorter = True
                    return True,None

                # 右子树为空的情况
                elif node.rchild == None:
                    node = node.lchild
                    self.shorter = True
                    if pre != None:
                        # 用来判断pre和node的关系
                        # left为True则node是pre的左子树,否则为右子树
                        left = False
                        if node.value < pre.value:
                            left = True

                        # 如果是左子树
                        if left:
                            pre.lchild = node.lchild
                        # 如果是右子树
                        else:
                            pre.rchild = node.lchild
                    else:
                        return True, node.lchild

                # 左子树为空的情况
                elif node.lchild == None:
                    node = node.rchild
                    self.shorter = True
                    if pre != None:
                        # 用来判断pre和node的关系
                        # left为True则node是pre的左子树,否则为右子树
                        left = False
                        if node.value < pre.value:
                            left = True

                        # 如果是左子树
                        if left:
                            pre.lchild = node.rchild
                        # 如果是右子树
                        else:
                            pre.rchild = node.rchild

                    else:
                        return True, node.rchild

                # 两个都不为空的情况
                else:
                    # 如果右子树比左子树高,找到右子树的最左节点
                    if node.balancefactor == -1:
                        # 寻找右子树的最左节点，然后递归删除最左节点
                        lc = node.rchild
                        while lc.lchild != None:
                            lc = lc.lchild
                        # 赋值，相当于删除
                        node.value = lc.value
                        # 递归删除右子树中最左子树值的节点，主要是为了保持平衡
                        DelNode(node, node.rchild, lc.value)
                    # 如果左子树高,找到左子树的最右节点
                    else:
                        rc = node.lchild
                        while rc.rchild != None:
                            rc = rc.rchild
                        node.value = rc.value
                        DelNode(node, node.lchild, rc.value)

            # 如果value小于当前节点的值，递归删除左子树
            elif value < node.value:
                result, node.lchild = DelNode(node, node.lchild, value)
                # 如果删除失败则返回false，node
                if result == False:
                    return False, node

                # 如果子树变矮了
                if self.shorter :
                    # 更新平衡因子
                    if node.balancefactor == 0:
                        node.balancefactor = -1
                        self.shorter = False
                    elif node.balancefactor == 1:
                        node.balancefactor = 0
                        self.shorter = True
                    # 如果平衡因子为-1
                    else:
                        # 如果右子树的平衡因子为0，不会改变当前树的深度
                        if node.rchild.balancefactor == 0:
                            self.shorter = False
                        # 如果右子树平衡因子不为0，深度会减少也就是node变矮了
                        else:
                            self.shorter = True
                        # 右平衡
                        
                        if node.value < pre.value:
                            pre.lchild = RightBalance(node)
                        else:
                            pre.rchild = RightBalance(node)

            # 如果value大于当前节点的值，递归删除右子树
            else:
                result, node.rchild = DelNode(node, node.rchild, value)
                # 如果删除失败则返回false，node
                if result == False:
                    return False, node

                # 如果子树变矮了
                if self.shorter :
                    # 更新平衡因子
                    if node.balancefactor == 0:
                        node.balancefactor = 1
                        self.shorter = False
                    elif node.balancefactor == -1:
                        node.balancefactor = 0
                        self.shorter = True
                    # 如果平衡因子为1
                    else:
                        # 如果左子树的平衡因子为0，不会改变当前树的深度
                        if node.lchild.balancefactor == 0:
                            self.shorter = False
                        # 如果左子树平衡因子不为0，深度会减少也就是node变矮了
                        else:
                            self.shorter = True
                        # 左平衡
                        if node.value < pre.value:
                            pre.lchild = LeftBalance(node)
                        else:
                            pre.rchild = LeftBalance(node)
            return True, node

        if string == 'root':
            self.root = DelNode(None, self.root, value)[1]
        elif string == 'anotherroot':
            self.anotherroot = DelNode(None, self.anotherroot, value)[1]

    def merge(self):
        # 合并两个平衡二叉树

        # 层次遍历需要的队列
        queue = []
        # 存放某个二叉树的数据
        lst = []

        # 层次遍历
        queue.append(self.anotherroot)

        while len(queue):
            node = queue.pop(0)
            lst.append(node.value)
            if node.lchild:
                queue.append(node.lchild)
            if node.rchild:
                queue.append(node.rchild)

        # 将lst中的元素插入到root中
        for element in lst:
            self.insert(element)

    def divide(self, x):
        # 通过x将一个平衡二叉树分开

        # 中序遍历需要的堆栈
        lst = []
        # 中序遍历得到的结果
        datas = []

        # 中序遍历获取数据
        root = self.root
        while root or len(lst):
            while root:
                lst.append(root)
                root = root.lchild

            if len(lst):
                root = lst.pop()
                datas.append(root)

            root = root.rchild

        # 找到x左右的下标
        index = 0
        while datas[index].value <= x and index < len(datas):
            index += 1

        # 插入到两个树中
        self.root = self.anotherroot = None
        for element in datas[0:index]:
            self.insert(element.value)

        for element in datas[index:]:
            self.insert(element.value, "anotherroot")


def main():
    Mytree = Tree()

    def show():
        # 通过debug插件实现二叉树可视化
        root = {
            "id": None,
            "value": None,
            "emphasizedValue": None,
            "children": []
        }

        def visual(tree, node):
            if tree == None:
                return
            else:
                node["id"] = tree.balancefactor
                node['value'] = tree.value

                left = {
                    "id": None,
                    "value": None,
                    "emphasizedValue": None,
                    "children": []
                }

                right = {
                    "id": None,
                    "value": None,
                    "emphasizedValue": None,
                    "children": []
                }
                node["children"].append(left)
                node["children"].append(right)
                visual(tree.lchild, left)
                visual(tree.rchild, right)

        visual(Mytree.root, root)

        graph = {
            "kind": {"tree": True},
            "root": root
        }
        json_graph = dumps(graph)
        pass
        print("aaa")

    def menu(order, Mytree):

        if order == 'insert':
            lst = []
            root = input("Please input the type of root(root/anotherroot)\n")
            answer = input('please input the value(-1 to end)\n')
            while answer != '-1':
                lst.append(int(answer))
                answer = input('please input the value(-1 to end)\n')

            for element in lst:
                Mytree.insert(element, root)

            if root == 'root':
                Mytree.show(Mytree.root)
            elif root == 'anotherroot':
                Mytree.show(Mytree.anotherroot)

        elif order == 'delete':
            lst = []
            root = input("Please input the type of root(root/anotherroot)\n")
            answer = input('please input the value(-1 to end)\n')
            while answer != '-1':
                lst.append(int(answer))
                answer = input('please input the value(-1 to end)\n')

            for element in lst:
                Mytree.delete(element, root)

            if root == 'root':
                Mytree.show(Mytree.root)
            elif root == 'anotherroot':
                Mytree.show(Mytree.anotherroot)

        elif order == 'merge':
            Mytree.merge()
            Mytree.show(Mytree.root)
        elif order == 'divide':
            x = int(input("Please input the x\n"))
            Mytree.divide(x)
            print("root:\n")
            Mytree.show(Mytree.root)
            print("anotherroot\n")
            Mytree.show(Mytree.anotherroot)

        elif order == 'show':
            Mytree.show()

    while True:
        order = input("insert,delete,merge,divide,show,exit\n")
        menu(order, Mytree)
        if order == 'exit':
            break
   

if __name__ == main():
    main()
